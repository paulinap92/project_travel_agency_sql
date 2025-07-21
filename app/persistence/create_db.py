import csv
import logging
from mysql.connector.pooling import MySQLConnectionPool
from mysql.connector import Error

# Default CSV path
CSV_FILE_PATH = 'app/data/trips_to_database.csv'

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _create_trips_table(cursor):
    """
    Creates the 'trips' table if it does not exist.
    """
    create_table_sql = """
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            destination VARCHAR(50) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            num_of_people INTEGER,
            agency_id INTEGER
        )
    """
    cursor.execute(create_table_sql)
    logger.info("Table 'trips' checked/created.")

def _validate_row(row, row_number):
    """
    Validates a single CSV row.
    Returns a tuple of validated values or None if validation fails.
    """
    if len(row) != 5:
        logger.warning(f"Row {row_number}: Invalid number of columns.")
        return None
    try:
        id_ = int(row[0]) if row[0] else None
        destination = str(row[1])
        price = float(row[2])
        num_of_people = int(row[3])
        agency_id = int(row[4])
        return id_, destination, price, num_of_people, agency_id
    except ValueError as e:
        logger.warning(f"Row {row_number}: Data type error - {e}")
        return None

def _insert_data_from_csv(connection, csv_file_path):
    """
    Inserts valid data from a CSV file into the 'trips' table.
    """
    inserted_rows = 0
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader, None)  # Skip header

        for row_number, row in enumerate(csv_reader, start=2):  # 2 = header + 1
            validated = _validate_row(row, row_number)
            if validated is None:
                continue

            with connection.cursor() as cursor:
                insert_sql = '''
                    INSERT INTO trips (id, destination, price, num_of_people, agency_id)
                    VALUES (%s, %s, %s, %s, %s)
                '''
                cursor.execute(insert_sql, validated)
                inserted_rows += 1

    logger.info(f"{inserted_rows} rows inserted from CSV.")

def create_tables(connection_pool: MySQLConnectionPool, csv_file_path: str = CSV_FILE_PATH):
    """
    Creates the 'trips' table and inserts data from a CSV file (if provided).
    """
    csv_file_path = csv_file_path or CSV_FILE_PATH

    try:
        with connection_pool.get_connection() as conn:
            if conn.is_connected():
                logger.info("Connected to the database.")
                with conn.cursor() as cursor:
                    _create_trips_table(cursor)
                    cursor.execute('SHOW TABLES')
                    logger.debug(f"Current tables: {cursor.fetchall()}")

                _insert_data_from_csv(conn, csv_file_path)
                conn.commit()
                logger.info("All changes committed.")
    except Error as e:
        logger.error(f"Database error during table creation or data insertion: {e}")

def drop_tables(connection_pool: MySQLConnectionPool):
    """
    Drops the 'trips' table from the database if it exists.
    """
    try:
        with connection_pool.get_connection() as conn:
            with conn.cursor() as cursor:
                drop_sql = "DROP TABLE IF EXISTS trips;"
                cursor.execute(drop_sql)
                logger.info("Table 'trips' dropped successfully.")
    except Error as e:
        logger.error(f"Error while dropping table: {e}")



