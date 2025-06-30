import pytest
from app.model.countries import Country, CountryConverter


def test_country_converter(countries_data_text, countries_converted_dict):
    converted_countries = CountryConverter().to_countries(countries_data_text)
    assert converted_countries == countries_converted_dict

