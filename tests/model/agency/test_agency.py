import pytest
from app.model.agency import Agency, AgencyConverter, AgencyRepo

def test_agency_creation(expected_agency_creation):
    agency = Agency(_id=1, _name="Travel Agency", _localization="New York")
    assert agency == expected_agency_creation

def test_agency_from_text_valid(agency_valid_line_from_text, expected_agency_creation):
    agency = Agency.from_text(agency_valid_line_from_text)
    assert agency == expected_agency_creation

def test_agency_from_text_invalid():
    invalid_data = "1,Travel Agency"
    with pytest.raises(AttributeError):
        Agency.from_text(invalid_data)

def test_agency_void():
    with pytest.raises(AttributeError):
        Agency.from_text('')


