import pytest
from app.model.countries import Country, CountryConverter, CountryRepo


@pytest.fixture
def expected_country_creation():
    return Country(name="Poland")


@pytest.fixture
def country_valid_line_from_text():
    return "Poland"


@pytest.fixture
def countries_data_text():
    return [
        "Poland",
        "Spain"
    ]

@pytest.fixture
def countries_data_set():
    return {
        "Poland",
        "Spain"
    }


@pytest.fixture
def countries_converted_dict():
    return {
        0: Country(name="Poland"),
        1: Country(name="Spain")
    }


@pytest.fixture
def mock_countries():
    country_1 = Country(name="Poland")
    country_2 = Country(name="Spain")
    return {1: country_1, 2: country_2}


@pytest.fixture
def country_repo(mock_countries):
    repo = CountryRepo(None)
    repo.countries = mock_countries
    return repo


# @pytest.fixture
# def agencies_converted_list():
#     return [
#         Agency(_id=1, _name="Agency One", _localization="London"),
#         Agency(_id=2, _name="Agency Two", _localization="Berlin"),
#     ]
