import logging
from app.persistence.create_db import create_tables, drop_tables
from app.persistence.connection import connection_pool
from app.service.agency_service import AgencyService
from app.persistence.dao import trip_db_dao
from app.model.agency import agency_repo
from app.model.countries import european_countries_repo

logging.basicConfig(level=logging.INFO)


def print_section(title: str, data: object) -> None:
    print(f"\n{'=' * 10} {title.upper()} {'=' * 10}")
    print(data)


def main() -> None:
    # Reset DB
    drop_tables(connection_pool)
    create_tables(connection_pool)

    # Init Service
    service = AgencyService(agency_repo, trip_db_dao)

    # Reports
    print_section("OFFER (agency → trips)", service.offer)
    print_section("AGENCY WITH MAX TRIPS", service.find_agency_with_max_trips())
    print_section("AGENCY WITH MAX INCOME", service.find_agency_with_max_income())
    print_section("COUNTRY WITH MAX TRIPS", service.find_country_with_max_trips())
    print_section("MAX TRIPS PER COUNTRY", service.report_agencies_with_max_trips_for_each_country())
    print_section("MEAN PRICE REPORT", service.mean_report_for_agencies())
    print_section("SELECTED EUROPEAN COUNTRIES", european_countries_repo.get_countries())
    print_section("TRIPS ONLY TO EUROPEAN COUNTRIES", service.report_only_selected_countries_trips(european_countries_repo))
    print_section("TRIPS BY PEOPLE QUANTITY", people_report := service.report_trips_for_people_quantity())
    print_section("MAX PRICE PER QUANTITY", service.report_max_price_for_quantity_report(people_report))


if __name__ == '__main__':
    main()
