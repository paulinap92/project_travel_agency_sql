# 🧳 Travel Agency Trips Analyzer

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-MySQL-blue?logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-blue?logo=docker&logoColor=white)
![Pipenv](https://img.shields.io/badge/Dependency%20Manager-Pipenv-9cf?logo=pipenv&logoColor=black)
![Pytest](https://img.shields.io/badge/Tested%20with-Pytest-yellow?logo=pytest)


> A powerful and extensible tool for analyzing travel agency trip data from text files and a MySQL database.

---

## 🚀 Project Overview

This project integrates travel agency data from text files and combines it with trip data stored in a MySQL database. It enables analytical reporting on:

- Agency performance
- Income generation
- Country-level statistics
- Group travel insights

### 📂 Data Sources

- **Agencies** (text file):
  - `Agency ID (int)`
  - `Agency name (string)`
  - `Agency location (string)`

- **Trips** (MySQL table):
  - `Trip ID (int)`
  - `Destination country (string)`
  - `Price per person (Decimal)`
  - `Number of people (int)`
  - `Agency ID (int)` — matches `Agency ID` from text file

> Note: There are no foreign key constraints; associations are handled in code.

---

## 🧠 Core Components

### `Agency`
- Data class representing a travel agency.

### `Trip`
- Data class for individual trip records.

### `AgencyService`
Encapsulates all business logic:

- Loads and connects agencies with trips
- Provides the following analyses:
  - ✅ Agency with the most trips
  - 💰 Agency with the highest income (with 19% VAT & 10% margin)
  - 🌍 Most visited countries
  - 📊 Average price reports and trip closest to average
  - 🏆 Agencies with most trips per country
  - 🇪🇺 Filter trips to selected countries (e.g., Europe)
  - 👥 Grouped price reports based on people count

---

## 🧪 Example Usage

```python
from app.persistence.create_db import create_tables, drop_tables
from app.persistence.connection import connection_pool
from app.service.agency_service import AgencyService
from app.persistence.dao import trip_db_dao
from app.model.agency import agency_repo
from app.model.countries import european_countries_repo
import logging

logging.basicConfig(level=logging.INFO)

def main() -> None:
    drop_tables(connection_pool)
    create_tables(connection_pool)

    service = AgencyService(agency_repo, trip_db_dao)

    print(service.offer)
    print(service.find_agency_with_max_trips())
    print(service.find_agency_with_max_income())
    print(service.find_country_with_max_trips())
    print(service.report_agencies_with_max_trips_for_each_country())
    print(service.mean_report_for_agencies())
    print(service.report_only_selected_countries_trips(european_countries_repo))
    people_report = service.report_trips_for_people_quantity()
    print(people_report)
    print(service.report_max_price_for_quantity_report(people_report))

if __name__ == '__main__':
    main()
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Install Dependencies

```bash
pipenv install
```

### 3. Start MySQL in Docker

Make sure Docker is running, then execute:

```bash
docker-compose up --build
```

This will start the MySQL database as defined in `docker-compose.yml`.

### 4. Run the Application

```bash
pipenv run python main.py
```

This drops and recreates the trips table and executes all reports.

### 5. Run Tests

```bash
pipenv run pytest
```

Or for specific test file:

```bash
pipenv run pytest tests/integration/test_integration.py
```

---

## ✅ Test Coverage

![Coverage](https://img.shields.io/badge/Coverage-100%25-success?logo=pytest)

This project has **100% test coverage** using `pytest` and `coverage.py`.

Run coverage with:

```bash
pipenv run pytest --cov=app --cov-report=term-missing
```

Generate HTML report:

```bash
pipenv run coverage html
open htmlcov/index.html

```

## Contact

![Email](https://img.shields.io/badge/Contact-paulina.piotrowska.p%40gmail.com-informational?logo=gmail)
