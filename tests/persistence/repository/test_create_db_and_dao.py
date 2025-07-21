import pytest
from decimal import Decimal
from mysql.connector.pooling import MySQLConnectionPool
from app.persistence.connection import MySQLConnectionPoolBuilder
from app.persistence.dao import TripDbDao
from app.persistence.model import Trip
from app.persistence.create_db import create_tables, drop_tables
import logging

# ---- Fixtures ----

@pytest.fixture(scope='module')
def connection_pool() -> MySQLConnectionPool:
    return MySQLConnectionPoolBuilder.builder().port(3308).build()

@pytest.fixture(scope='module', autouse=True)
def setup_database(connection_pool):
    logging.info("Creating tables before tests")
    drop_tables(connection_pool)
    create_tables(connection_pool)
    yield
    logging.info("Dropping tables after tests")
    drop_tables(connection_pool)

@pytest.fixture
def trip_dao(connection_pool):
    return TripDbDao(connection_pool)

@pytest.fixture
def valid_trip():
    return Trip(
        _destination="Madrid",
        _price=Decimal("999.99"),
        _num_of_people=2,
        _agency_id=1
    )

@pytest.fixture
def invalid_trip():
    return Trip(
        _destination="123###",
        _price=Decimal("-100.00"),
        _num_of_people=-5,
        _agency_id=1
    )

# ---- Tests ----
@pytest.mark.integration
class TestTripDbDao:

    def test_insert_valid_trip(self, trip_dao, valid_trip):
        trip_id = trip_dao.insert(valid_trip)
        assert trip_id > 0

        row = trip_dao.find_by_id(trip_id)
        assert row is not None
        assert row[1] == valid_trip.destination
        assert row[2] == valid_trip.price
        assert row[3] == valid_trip.num_of_people
        assert row[4] == valid_trip.agency_id

    def test_find_all_after_insert(self, trip_dao, valid_trip):
        trip_dao.insert(valid_trip)
        trips = trip_dao.find_all()
        assert any(t.destination == valid_trip.destination for t in trips)

    def test_find_all_valid(self, trip_dao, invalid_trip):
        trip_dao.insert(invalid_trip)
        valid_trips = trip_dao.find_all_valid()
        for trip in valid_trips:
            assert trip.destination is not None
            assert trip.destination.replace(" ", "").isalpha()
            assert trip.price is not None and trip.price >= 0
            assert trip.num_of_people is not None and trip.num_of_people >= 0

    def test_find_by_agency_id(self, trip_dao, valid_trip):
        trip_dao.insert(valid_trip)
        results = trip_dao.find_by_agency_id(valid_trip.agency_id)
        assert isinstance(results, list)
        assert any(row[4] == valid_trip.agency_id for row in results)

    def test_count_trips_per_countries(self, trip_dao, valid_trip):
        trip_dao.insert(valid_trip)
        counts = trip_dao.count_trips_per_countries()
        assert isinstance(counts, list)
        assert any(destination == valid_trip.destination for destination, _ in counts)

    def test_countries_with_max_trips_for_agency(self, trip_dao):
        results = trip_dao.countries_with_max_trips_for_agency()
        assert isinstance(results, list)
        if results:
            assert len(results[0]) == 3  # destination, agency_id, trip_count

    def test_update_trip(self, trip_dao, valid_trip):
        trip_id = trip_dao.insert(valid_trip)
        updated = Trip(
            _destination="Barcelona",
            _price=valid_trip.price,
            _num_of_people=valid_trip.num_of_people,
            _agency_id=valid_trip.agency_id
        )
        trip_dao.update(trip_id, updated)
        updated_trip = trip_dao.find_by_id(trip_id)
        assert updated_trip[1] == "Barcelona"

    def test_find_by_id(self, trip_dao, valid_trip):
        inserted_id = trip_dao.insert(valid_trip)
        result = trip_dao.find_by_id(inserted_id)
        assert result is not None
        assert result[1] == valid_trip.destination

    def test_delete_by_id(self, trip_dao, valid_trip):
        trip_id = trip_dao.insert(valid_trip)
        trip_dao.delete(trip_id)
        result = trip_dao.find_by_id(trip_id)
        assert result is None or result == ()

    def test_find_all_as_dict(self, trip_dao, valid_trip):
        trip_dao.insert(valid_trip)
        result = trip_dao.find_all_as_dict()
        assert isinstance(result, dict)
        for k, v in result.items():
            assert isinstance(k, int)
            assert isinstance(v, Trip)

    def test_insert_many_and_find_all(self, trip_dao):
        trips = [
            Trip(_destination="Paris", _price=Decimal("800.00"), _num_of_people=1, _agency_id=2),
            Trip(_destination="Berlin", _price=Decimal("750.50"), _num_of_people=3, _agency_id=2),
        ]
        trip_dao.insert_many(trips)

        results = trip_dao.find_all()
        destinations = [trip.destination for trip in results]
        assert "Paris" in destinations
        assert "Berlin" in destinations

    def test_delete_all(self, trip_dao):
        trip_dao.delete_all()
        results = trip_dao.find_all()
        assert results == []