import logging
from typing import Any
from mysql.connector.pooling import MySQLConnectionPool
from datetime import date, datetime
from abc import ABC
from decimal import Decimal
import re
import inflection

from app.persistence.model import Trip
from app.persistence.connection import connection_pool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CrudDao(ABC):
    """Base class for CRUD operations on a database table."""

    def __init__(self, connection_pool: MySQLConnectionPool, entity: Any):
        """Initializes the DAO with a connection pool and entity type.

        Args:
            connection_pool (MySQLConnectionPool): MySQL connection pool.
            entity (Any): A class representing the database entity.
        """
        self._connection_pool = connection_pool
        self._entity = entity
        self._entity_type = type(entity())

    def insert(self, item: Any) -> int:
        """Inserts a single item into the database.

        Args:
            item (Any): The entity object to insert.

        Returns:
            int: ID of the inserted row.
        """
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            sql = (f'INSERT INTO {self._table_name()} ({self._column_names_for_insert()}) '
                   f'VALUES ({self._column_values_for_insert(item)})')
            logger.info(f"[SQL] {sql}")
            cursor.execute(sql)
            conn.commit()
            return cursor.lastrowid

    def insert_many(self, items: list[Any]) -> int:
        """Inserts multiple items into the database.

        Args:
            items (list[Any]): List of entity objects.

        Returns:
            int: ID of the last inserted row.
        """
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            values = ", ".join([f'({CrudDao._column_values_for_insert(item)})' for item in items])
            sql = (f'INSERT INTO {self._table_name()} ({self._column_names_for_insert()}) '
                   f'VALUES {values}')
            logger.info(f"[SQL] {sql}")
            cursor.execute(sql)
            conn.commit()
            return cursor.lastrowid

    def update(self, id_: int, item: Any) -> int:
        """Updates a record in the database by ID.

        Args:
            id_ (int): The ID of the record to update.
            item (Any): The updated entity object.

        Returns:
            int: The same ID passed in.
        """
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            sql = (f'UPDATE {self._table_name()} '
                   f'SET {CrudDao._column_names_and_values_for_update(item)} '
                   f'WHERE id={id_}')
            logger.info(f"[SQL] {sql}")
            cursor.execute(sql)
            conn.commit()
            return id_

    def find_all(self) -> list[Any]:
        """Fetches all records from the table.

        Returns:
            list[Any]: List of entity objects.
        """
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            sql = f'SELECT * FROM {self._table_name()}'
            logger.info(f"[SQL] {sql}")
            cursor.execute(sql)
            return [self._entity(*row) for row in cursor.fetchall()]

    def find_all_as_dict(self) -> dict[int, Any]:
        """Fetches all records and returns them as a dictionary keyed by ID.

        Returns:
            dict[int, Any]: Dictionary of entity objects.
        """
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            sql = f'SELECT * FROM {self._table_name()}'
            logger.info(f"[SQL] {sql}")
            cursor.execute(sql)
            result = {row[0]: self._entity(*row) for row in cursor.fetchall()}
            return result

    def find_by_id(self, id_: int) -> Any:
        """Fetches a record by its ID.

        Args:
            id_ (int): Record ID.

        Returns:
            Any: Entity object or None.
        """
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            sql = f'SELECT * FROM {self._table_name()} WHERE id={id_}'
            logger.info(f"[SQL] {sql}")
            cursor.execute(sql)
            return cursor.fetchone()

    def delete(self, id_: int) -> int:
        """Deletes a record by ID.

        Args:
            id_ (int): Record ID.

        Returns:
            int: Deleted record ID.
        """
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            sql = f'DELETE FROM {self._table_name()} WHERE id={id_}'
            logger.info(f"[SQL] {sql}")
            cursor.execute(sql)
            conn.commit()
            return id_

    def delete_all(self) -> None:
        """Deletes all records from the table."""
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            sql = f'DELETE FROM {self._table_name()} WHERE id>0'
            logger.info(f"[SQL] {sql}")
            cursor.execute(sql)
            conn.commit()

    # --------------------------------------------------------------------
    # SQL helper methods
    # --------------------------------------------------------------------

    def _table_name(self) -> str:
        """Returns the table name based on the entity class name."""
        return inflection.tableize(self._entity_type.__name__)

    def _field_names(self) -> list[str]:
        """Returns a list of field names from the entity class."""
        return self._entity().__dict__.keys()

    def _column_names_for_insert(self) -> str:
        """Returns column names for SQL INSERT, excluding '_id'."""
        fields = [field.lstrip('_') for field in self._field_names() if field.lower() != '_id']
        return ', '.join(fields)

    @staticmethod
    def _to_str(value: Any) -> str:
        """Converts a Python value to SQL-safe string."""
        return f"'{value}'" if isinstance(value, (str, datetime, date)) else str(value)

    @staticmethod
    def _column_values_for_insert(item: Any) -> str:
        """Generates column values for SQL INSERT."""
        return ', '.join([
            CrudDao._to_str(value)
            for field, value in item.__dict__.items()
            if field.lower() != '_id'
        ])

    @staticmethod
    def _column_names_and_values_for_update(item: Any) -> str:
        """Generates `column=value` pairs for SQL UPDATE, skipping nulls and ID."""
        return ', '.join([
            f'{field.lstrip("_")}={CrudDao._to_str(value)}'
            for field, value in item.__dict__.items()
            if field.lower() != 'id' and value is not None
        ])


class TripDbDao(CrudDao):
    """Data access object for Trip entities."""

    def __init__(self, connection_pool: MySQLConnectionPool):
        """Initializes the DAO with Trip as the entity."""
        super().__init__(connection_pool, Trip)

    def find_all_valid(self) -> list[Trip]:
        """Fetches all trips that pass validation rules.

        Returns:
            list[Trip]: List of valid Trip entities.
        """
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            sql = f'SELECT * FROM {self._table_name()}'
            logger.info(f"[SQL] {sql}")
            cursor.execute(sql)
            rows = cursor.fetchall()

        valid_results = []
        for row in rows:
            entity = self._entity(*row)

            is_valid_destination = entity._destination and re.fullmatch(r'^[A-Za-z\s]+$', entity._destination)
            is_valid_price = entity._price is not None and isinstance(entity._price, Decimal) and entity._price >= Decimal('0')
            is_valid_num_of_people = entity._num_of_people is not None and isinstance(entity._num_of_people, int) and entity._num_of_people >= 0

            if is_valid_destination and is_valid_price and is_valid_num_of_people:
                valid_results.append(entity)
            else:
                logger.warning(f"Invalid record: {entity}")

        return valid_results

    def find_by_agency_id(self, agency_id: int) -> list[Trip]:
        """Finds trips for a specific agency ID.

        Args:
            agency_id (int): ID of the travel agency.

        Returns:
            list[Trip]: List of matching Trip records.
        """
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            sql = f'SELECT * FROM {self._table_name()} WHERE agency_id={agency_id}'
            logger.info(f"[SQL] {sql}")
            cursor.execute(sql)
            return cursor.fetchall()

    def count_trips_per_countries(self) -> list[tuple[str, int]]:
        """Counts number of trips per destination.

        Returns:
            list[tuple[str, int]]: Destination and number of trips.
        """
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            sql = '''
                SELECT destination, COUNT(*) AS number_of_trips 
                FROM trips 
                GROUP BY destination 
                ORDER BY number_of_trips DESC
            '''
            logger.info(f"[SQL] {sql.strip()}")
            cursor.execute(sql)
            return cursor.fetchall()

    def countries_with_max_trips_for_agency(self) -> list[tuple[str, int, int]]:
        """Finds the agency with the most trips per destination.

        Returns:
            list[tuple[str, int, int]]: destination, agency_id, number of trips
        """
        with self._connection_pool.get_connection() as conn:
            cursor = conn.cursor()
            sql = '''
                WITH TripCounts AS (
                    SELECT destination, agency_id, COUNT(*) AS trip_count
                    FROM trips
                    GROUP BY destination, agency_id
                ),
                MaxTrips AS (
                    SELECT destination, MAX(trip_count) AS max_trip_count
                    FROM TripCounts
                    GROUP BY destination
                )
                SELECT t.destination, t.agency_id, t.trip_count 
                FROM TripCounts t
                JOIN MaxTrips m ON t.destination = m.destination AND t.trip_count = m.max_trip_count
                ORDER BY t.destination, t.agency_id
            '''
            logger.info(f"[SQL] {sql.strip()}")
            cursor.execute(sql)
            return cursor.fetchall()


# Instantiate the DAO
trip_db_dao = TripDbDao(connection_pool)
