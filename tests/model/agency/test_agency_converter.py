import pytest
from app.model.agency import Agency, AgencyConverter


def test_agency_converter(agencies_data_text, agencies_converted_dict):
    converted_agencies = AgencyConverter().to_agencies(agencies_data_text)
    assert converted_agencies == agencies_converted_dict

