import pytest
from unittest.mock import MagicMock, patch

from app.model.agency import Agency, AgencyConverter, AgencyRepo
from app.file_manager.file_manager import FileManager


def test_get_agencies(agency_repo, mock_agencies):
    agencies = agency_repo.get_agencies()
    assert len(agencies) == len(mock_agencies)
    assert agencies[0]._name == "Agency One"
    assert agencies[1]._name == "Agency Two"


def test_id_agencies(agency_repo, mock_agencies):
    assert agency_repo.get_by_id(1) == Agency(
        _id=1, _name="Agency One", _localization="New York"
    )
    assert agency_repo.agency_name_for_id(1) == "Agency One"


@patch("app.file_manager.file_manager.FileManager._create_file_method")
@patch("app.model.agency.AgencyConverter.to_agencies")
def test_read_file(mock_to_agencies, mock_create_file_method):
    mock_create_file_method.return_value = MagicMock(
        return_value=["1,Travel Agency,New York"]
    )

    mock_to_agencies.return_value = {
        1: Agency(_id=1, _name="Travel Agency", _localization="New York")
    }

    repo = AgencyRepo("path.txt")

    expected = {
        1: Agency(_id=1, _name="Travel Agency", _localization="New York")
    }

    assert repo.agencies == expected
