from app.persistence.create_db import create_tables, drop_tables
from app.persistence.connection import  connection_pool
from app.service.agency_service import AgencyService
import logging
from app.persistence.dao import trip_db_dao
from app.model.agency import agency_repo
from app.model.countries import european_countries_repo

logging.basicConfig(level=logging.INFO)

def main() -> None:
    drop_tables(connection_pool)
    create_tables(connection_pool)

    off = AgencyService(agency_repo, trip_db_dao)

    print(off.offer)
    print(off.find_agency_with_max_trips())
    print('***income***')
    print(off.find_agency_with_max_income())
    print('***country with max trips***')
    print(off.find_country_with_max_trips())
    print('***report agencies with max trips for each country***')
    print(off.report_agencies_with_max_trips_for_each_country())
    print('***mean report***')
    print(off.mean_report_for_agencies())
    print('***european countires report report***')
    print(european_countries_repo.countries)
    print(off.report_only_selected_countries_trips(european_countries_repo))
    print('***people quantity report***')
    print(report := off.report_trips_for_people_quantity())
    print('***max price for people quantity report***')
    print(off.report_max_price_for_quantity_report(report))

if __name__ == '__main__':
    main()