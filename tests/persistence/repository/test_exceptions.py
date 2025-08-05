import pytest
import os
import tempfile
from app.persistence.create_db import _validate_row, create_tables, drop_tables
from app.persistence.connection import MySQLConnectionPoolBuilder
from mysql.connector.errors import InterfaceError
from unittest.mock import MagicMock, patch
from mysql.connector import Error

def test_validate_row_invalid_column_count(caplog):
    row = ["1", "Madrid", "1000"]
    result = _validate_row(row, row_number=1)
    assert result is None
    assert "Invalid number of columns" in caplog.text


def test_validate_row_invalid_data_type(caplog):
    row = ["abc", "Madrid", "xyz", "five", "NaN"]
    result = _validate_row(row, row_number=2)
    assert result is None
    assert "Data type error" in caplog.text


def test_insert_data_from_csv_skips_invalid_rows(monkeypatch, caplog):
    content = "id,destination,price,num_of_people,agency_id\n" \
              "1,Madrid,1000.00,2,1\n" \
              "2,Madrid,INVALID,2,1\n" \
              "3,,1000.00,2\n"  # za mało kolumn

    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp_csv:
        tmp_csv.write(content)
        tmp_csv_path = tmp_csv.name

    try:
        pool = MySQLConnectionPoolBuilder.builder().port(3308).build()
        create_tables(pool, csv_file_path=tmp_csv_path)

        assert "Data type error" in caplog.text
        assert "Invalid number of columns" in caplog.text
        assert "rows inserted from CSV" in caplog.text
    finally:
        os.remove(tmp_csv_path)


def test_create_tables_database_error(caplog):
    # Przygotowanie: fałszywy connection_pool, który podnosi wyjątek
    fake_pool = MagicMock()
    fake_conn = MagicMock()
    fake_pool.get_connection.side_effect = Error("Mocked DB error")

    with caplog.at_level("ERROR"):
        create_tables(fake_pool, csv_file_path="dummy.csv")

    assert any("Database error during table creation or data insertion" in message for message in caplog.text.splitlines())


def test_drop_tables_database_error(caplog):
    fake_pool = MagicMock()
    fake_pool.get_connection.side_effect = Error("Mocked drop error")

    with caplog.at_level("ERROR"):
        drop_tables(fake_pool)

    assert any("Error while dropping table: Mocked drop error" in message for message in caplog.text.splitlines())
