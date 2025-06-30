import pytest
from app.model.countries import Country, CountryConverter, CountryRepo

def test_country_creation(expected_country_creation):
    country = Country(name="Poland")
    assert country == expected_country_creation

def test_country_from_text_valid(country_valid_line_from_text, expected_country_creation):
    country =   Country.from_text(country_valid_line_from_text)
    assert country == expected_country_creation

def test_country_from_text_invalid():
    invalid_data = "1,COUNTRY,47364"
    with pytest.raises(AttributeError):
        Country.from_text(invalid_data)

def test_country_void():
    with pytest.raises(AttributeError):
        Country.from_text('')


