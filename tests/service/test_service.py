import pytest
from decimal import Decimal
from unittest.mock import MagicMock
from app.model.agency import Agency
from app.service.agency_service import AgencyService
from app.persistence.model import Trip




def test_find_agency_with_max_trips(service, sample_agencies):
    result = service.find_agency_with_max_trips()
    assert result == [(sample_agencies[1], 2)]


def test_find_agency_with_max_income(service, sample_agencies):
    result = service.find_agency_with_max_income()
    assert result[0][0] == sample_agencies[1]
    assert isinstance(result[0][1], Decimal)


def test_find_country_with_max_trips(service):
    result = service.find_country_with_max_trips()
    assert result == [("Spain", 2)]


def test_mean_report_for_agencies(service):
    report = service.mean_report_for_agencies()
    assert "TravelPlus" in report
    mean_price, closest_trip = report["TravelPlus"]
    assert isinstance(mean_price, Decimal)
    assert isinstance(closest_trip, Trip)


def test_report_agencies_with_max_trips_for_each_country(service):
    result = service.report_agencies_with_max_trips_for_each_country()
    assert result == {
        "Spain": ["TravelPlus"],
        "Italy": ["GoHoliday"]
    }


def test_report_only_selected_countries_trips(service):
    country_repo = MagicMock()
    country_repo.get_countries.return_value = {"Spain"}
    result = service.report_only_selected_countries_trips(country_repo)
    assert all(trip.destination == "Spain" for trip in result)


def test_report_trips_for_people_quantity(service):
    result = service.report_trips_for_people_quantity()
    assert isinstance(result, dict)
    assert all(isinstance(k, int) for k in result.keys())


def test_report_max_price_for_quantity_report(service):
    quantity_report = service.report_trips_for_people_quantity()
    result = service.report_max_price_for_quantity_report(quantity_report)
    assert isinstance(result, dict)
    assert all(isinstance(v, list) for v in result.values())


def test_count_income_for_trips():
    trip1 = MagicMock()
    trip2 = MagicMock()
    trip1.get_income.return_value = Decimal("100.50")
    trip2.get_income.return_value = Decimal("200.75")

    result = AgencyService._count_income_for_trips([trip1, trip2])
    assert result == Decimal("301.25")


def test_mean_price_for_trips():
    trip1 = Trip(_agency_id=1, _price=Decimal("100"), _destination="Spain", _num_of_people=2)
    trip2 = Trip(_agency_id=1, _price=Decimal("200"), _destination="Spain", _num_of_people=2)

    result = AgencyService._mean_price_for_trips([trip1, trip2])
    assert result == Decimal("150")

def test_mean_price_for_empty_trips():
    result = AgencyService._mean_price_for_trips([])
    assert result == Decimal("0")


def test_find_agency_with_max_trips_empty():
    service = AgencyService(agency_repo=MagicMock(), trip_db_dao=MagicMock(), offer={})
    result = service.find_agency_with_max_trips()
    assert result == []