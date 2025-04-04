import pytest
from app.model.agency import Agency, AgencyConverter, AgencyRepo


@pytest.fixture
def expected_agency_creation():
    return Agency(_id=1, _name="Travel Agency", _localization="New York")


@pytest.fixture
def agency_valid_line_from_text():
    return "1,Travel Agency,New York"


@pytest.fixture
def agencies_data_text():
    return [
        "1,Agency One,London",
        "2,Agency Two,Berlin",
        "3,Agency Three,Prague",
    ]


@pytest.fixture
def agencies_converted_dict():
    return {
        1: Agency(_id=1, _name="Agency One", _localization="London"),
        2: Agency(_id=2, _name="Agency Two", _localization="Berlin"),
        3: Agency(_id=3, _name="Agency Three", _localization="Prague"),
    }


@pytest.fixture
def mock_agencies():
    agency_1 = Agency(_id=1, _name="Agency One", _localization="New York")
    agency_2 = Agency(_id=2, _name="Agency Two", _localization="New York")
    return {1: agency_1, 2: agency_2}


@pytest.fixture
def agency_repo(mock_agencies):
    repo = AgencyRepo(None)
    repo.agencies = mock_agencies
    return repo


@pytest.fixture
def agencies_converted_list():
    return [
        Agency(_id=1, _name="Agency One", _localization="London"),
        Agency(_id=2, _name="Agency Two", _localization="Berlin"),
    ]
