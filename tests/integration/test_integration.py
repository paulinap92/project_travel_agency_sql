import pytest
from decimal import Decimal
from collections import defaultdict
from app.service.agency_service import AgencyService
from app.model.agency import Agency
from app.persistence.model import Trip
from app.model.countries import CountryRepo

class FakeAgencyRepo:
    def __init__(self):
        self.agencies = {
            1: Agency(_id=1, _name="Best Travels", _localization="City A"),
            2: Agency(_id=2, _name="Sunny Tours", _localization="City B"),
        }
    def get_by_id(self, agency_id):
        return self.agencies.get(agency_id)

    def agency_name_for_id(self, agency_id):
        agency = self.agencies.get(agency_id)
        return agency._name if agency else "Unknown agency"

class FakeTripDbDao:
    def __init__(self):
        # Teraz obie agencje mają po 2 wycieczki, żeby test na max trips przechodził
        self.trips = [
            Trip(_id=1, _destination="Paris", _price=Decimal("1000"), _num_of_people=2, _agency_id=1),
            Trip(_id=2, _destination="Rome", _price=Decimal("800"), _num_of_people=4, _agency_id=1),
            Trip(_id=3, _destination="London", _price=Decimal("1200"), _num_of_people=1, _agency_id=2),
            Trip(_id=4, _destination="Berlin", _price=Decimal("900"), _num_of_people=3, _agency_id=2),
        ]

    def find_all_valid(self):
        return self.trips

    def count_trips_per_countries(self):
        return [("France", 2), ("Italy", 3)]

    def countries_with_max_trips_for_agency(self):
        return [("France", 1), ("Italy", 2)]

    def find_all(self):
        return self.trips

class FakeCountryRepo:
    def get_countries(self):
        return ["Paris", "London", "Berlin"]

@pytest.fixture
def fake_agency_repo():
    return FakeAgencyRepo()

@pytest.fixture
def fake_trip_db_dao():
    return FakeTripDbDao()

@pytest.fixture
def fake_country_repo():
    return FakeCountryRepo()

class TestIntegrationAgencyService:
    def test_agency_service_basic_flow(self, fake_agency_repo, fake_trip_db_dao):
        service = AgencyService(fake_agency_repo, fake_trip_db_dao)

        max_trips_agencies = service.find_agency_with_max_trips()
        assert any(agency._name == "Best Travels" for agency, _ in max_trips_agencies)
        assert any(agency._name == "Sunny Tours" for agency, _ in max_trips_agencies)

        max_income_agencies = service.find_agency_with_max_income()
        assert max_income_agencies  # nie jest puste
        assert all(isinstance(income, Decimal) for _, income in max_income_agencies)

        country_max_trips = service.find_country_with_max_trips()
        assert ("Italy", 3) in country_max_trips

        mean_report = service.mean_report_for_agencies()
        assert "Best Travels" in mean_report
        assert "Sunny Tours" in mean_report

        max_trips_per_country = service.report_agencies_with_max_trips_for_each_country()
        assert "France" in max_trips_per_country
        assert "Italy" in max_trips_per_country
