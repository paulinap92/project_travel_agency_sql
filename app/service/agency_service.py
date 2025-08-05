from app.model.agency import AgencyRepo, Agency
from app.persistence.dao import TripDbDao
from app.persistence.model import Trip
from collections import defaultdict
from decimal import Decimal
from typing import Any
from dataclasses import dataclass, field
from app.model.countries import CountryRepo


@dataclass
class AgencyService:
    """Service class for analyzing and reporting on travel agencies and their trips.

    Attributes:
        agency_repo (AgencyRepo): Repository for retrieving agency data.
        trip_db_dao (TripDbDao): DAO for accessing trip data.
        offer (dict[Agency, list[Trip]]): Mapping of agencies to their valid trips.
    """

    agency_repo: AgencyRepo
    trip_db_dao: TripDbDao
    offer: dict[Agency, list[Trip]] = field(default_factory=dict)

    def __post_init__(self):
        """Initializes the offer dictionary by grouping valid trips by agency."""
        agencies = self.agency_repo
        trips = self.trip_db_dao.find_all_valid()
        grouped_by_agency_id = defaultdict(list)
        for trip in trips:
            grouped_by_agency_id[agencies.get_by_id(trip.agency_id)].append(trip)
        self.offer = grouped_by_agency_id

    def find_agency_with_max_trips(self) -> list[tuple[Agency, int]]:
        """Finds the agency or agencies with the highest number of trips.

        Returns:
            list[tuple[Agency, int]]: A list of (agency, number_of_trips) tuples.
        """
        if not self.offer:
            return []

        max_trips = max(len(v) for v in self.offer.values())
        return [(k, len(v)) for k, v in self.offer.items() if len(v) == max_trips]

    @staticmethod
    def _count_income_for_trips(trips: list[Trip]) -> Decimal:
        """Calculates total income from a list of trips.

        Args:
            trips (list[Trip]): List of trips.

        Returns:
            Decimal: Total income from the trips.
        """
        return sum((trip.get_income() for trip in trips), Decimal('0'))

    def find_agency_with_max_income(self) -> list[tuple[Agency, Decimal]]:
        """Finds the agency or agencies with the highest income.

        Returns:
            list[tuple[Agency, Decimal]]: A list of (agency, income) tuples.
        """
        incomes = defaultdict(Decimal)
        for agency, trips in self.offer.items():
            incomes[agency] = AgencyService._count_income_for_trips(trips)
        max_income = max(incomes.values(), default=Decimal(0))
        return [(agency, income) for agency, income in incomes.items() if income == max_income]

    def find_country_with_max_trips(self) -> list[tuple[str, int]]:
        """Finds the country or countries with the highest number of trips.

        Returns:
            list[tuple[str, int]]: A list of (country_name, number_of_trips) tuples.
        """
        trips_per_countries = self.trip_db_dao.count_trips_per_countries()
        max_trips = max(trips_per_countries, key=lambda x: x[1])[1]
        return [trip for trip in trips_per_countries if trip[1] == max_trips]

    @staticmethod
    def _mean_price_for_trips(trips: list[Trip]) -> Decimal:
        """Calculates the average price of a list of trips.

        Args:
            trips (list[Trip]): List of trips.

        Returns:
            Decimal: Mean price. Returns 0 if the list is empty.
        """
        if not trips:
            return Decimal("0")
        total_price = sum(trip.price for trip in trips)
        return Decimal(total_price / len(trips))

    def mean_report_for_agencies(self) -> defaultdict[Any, tuple[Decimal, Trip]]:
        """Generates a report of the average trip price per agency and the trip closest to this average.

        Returns:
            defaultdict[str, tuple[Decimal, Trip]]: A mapping of agency name to (mean price, closest trip).
        """
        report = defaultdict(tuple)
        for agency, trips in self.offer.items():
            mean_price = AgencyService._mean_price_for_trips(trips)
            min_dif = min(trips, key=lambda trip: abs(trip.price - mean_price))
            report[agency.name] = (mean_price, min_dif)
        return report

    def report_agencies_with_max_trips_for_each_country(self) -> dict[str, list[str]]:
        """Generates a report of the top-performing agency or agencies per country.

        Returns:
            dict[str, list[str]]: A mapping of country name to list of top agency names.
        """
        grouped_by_country = defaultdict(list)
        countries = self.trip_db_dao.countries_with_max_trips_for_agency()
        for country in countries:
            grouped_by_country[country[0]].append(self.agency_repo.agency_name_for_id(int(country[1])))
        return grouped_by_country

    def report_only_selected_countries_trips(self, countries: CountryRepo) -> list[Trip]:
        """Filters trips to only include those with destinations in selected countries.

        Args:
            countries (CountryRepo): Repository providing the list of selected countries.

        Returns:
            list[Trip]: Filtered list of trips.
        """
        european_countries = countries.get_countries()
        trips = self.trip_db_dao.find_all_valid()
        return [trip for trip in trips if trip.destination in european_countries]

    def report_trips_for_people_quantity(self) -> dict[int, set[Trip]]:
        """Groups trips by the number of people.

        Returns:
            dict[int, set[Trip]]: A mapping of number_of_people to set of trips.
        """
        trips = self.trip_db_dao.find_all()
        grouped_trips = defaultdict(set)
        for trip in trips:
            grouped_trips[trip.num_of_people].add(trip)
        return grouped_trips

    def report_max_price_for_quantity_report(self, report: dict[int, set[Trip]]) -> dict[int, list[Trip]]:
        """From a quantity-based report, finds trips with the maximum price for each group.

        Args:
            report (dict[int, set[Trip]]): A mapping of number_of_people to set of trips.

        Returns:
            dict[int, list[Trip]]: A mapping of number_of_people to list of trips with max price,
            sorted by price-per-person in descending order.
        """
        grouped_trips_max_price = defaultdict(list)
        for key, value in report.items():
            max_price = max(value, key=lambda x: x.price)
            grouped_trips_max_price[key] = [trip for trip in value if trip.price == max_price.price]

        return dict(sorted(
            grouped_trips_max_price.items(),
            key=lambda item: item[1][0].price / item[0],
            reverse=True
        ))
