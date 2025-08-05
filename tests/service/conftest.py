import pytest
from decimal import Decimal
from unittest.mock import MagicMock
from app.model.agency import Agency
from app.service.agency_service import AgencyService
from app.persistence.model import Trip


@pytest.fixture
def sample_agencies():
    return {
        1: Agency(1, "TravelPlus", "Warsaw"),
        2: Agency(2, "GoHoliday", "Krakow"),
    }

@pytest.fixture
def sample_trips():
    return [
        Trip(_id=1, _destination="Spain", _price=Decimal("1000.00"), _num_of_people=2, _agency_id=1),
        Trip(_id=2, _destination="Italy", _price=Decimal("1500.00"), _num_of_people=4, _agency_id=1),
        Trip(_id=3, _destination="Spain", _price=Decimal("900.00"), _num_of_people=1, _agency_id=2),
    ]


@pytest.fixture
def mocked_agency_repo(sample_agencies):
    mock = MagicMock()
    mock.get_by_id.side_effect = lambda x: sample_agencies.get(x)
    mock.agency_name_for_id.side_effect = lambda x: sample_agencies.get(x).name
    return mock


@pytest.fixture
def mocked_trip_dao(sample_trips):
    mock = MagicMock()
    mock.find_all_valid.return_value = sample_trips
    mock.find_all.return_value = sample_trips
    mock.count_trips_per_countries.return_value = [("Spain", 2), ("Italy", 1)]
    mock.countries_with_max_trips_for_agency.return_value = [("Spain", 1), ("Italy", 2)]
    return mock


@pytest.fixture
def service(mocked_agency_repo, mocked_trip_dao):
    return AgencyService(agency_repo=mocked_agency_repo, trip_db_dao=mocked_trip_dao)
