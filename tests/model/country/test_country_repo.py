import pytest
from unittest.mock import MagicMock, patch

from app.model.countries import Country, CountryConverter, CountryRepo
from app.file_manager.file_manager import FileManager


def test_get_countries(country_repo, countries_data_set):
    countries = country_repo.get_countries()
    assert countries == countries_data_set



@patch("app.file_manager.file_manager.FileManager._create_file_method")
@patch("app.model.countries.CountryConverter.to_countries")
def test_read_file(mock_to_countries, mock_create_file_method):
    mock_create_file_method.return_value = MagicMock(
        return_value=["Poland"]
    )

    mock_to_countries.return_value = {
        1: Country(name="Poland")
    }

    repo = CountryRepo("path.txt")

    expected = {
        1: Country(name="Poland")
    }

    assert repo.countries == expected
