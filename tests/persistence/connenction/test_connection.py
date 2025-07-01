from app.persistence.connection import MySQLConnectionPoolBuilder
from mysql.connector.errors import DatabaseError
import pytest

class TestConnectionBuilder:

    def test_when_builder_dict_structure_has_expected_items(self):
        builder = MySQLConnectionPoolBuilder.builder().pool_size(10).port(3308).user("admin").password("pass").database("db")
        config = builder._pool_config
        assert config['port'] == 3308
        assert config['user'] == "admin"
        assert config['password'] == "pass"
        assert config['database'] == "db"
        assert config['pool_name'] == "my_pool"
        assert config['pool_size'] == 10
        assert config['host'] == "localhost"

    def test_default_config_is_used_when_no_params_passed(self):
        builder = MySQLConnectionPoolBuilder()
        config = builder._pool_config
        assert config['port'] == 3307
        assert config['user'] == "user"
        assert config['password'] == "user1234"
        assert config['database'] == "db_1"
        assert config['pool_name'] == "my_pool"
        assert config['pool_size'] == 5
        assert config['host'] == "localhost"

    def test_when_connection_builder_works(self):
        connection_pool = MySQLConnectionPoolBuilder.builder().port(3308).build()
        assert connection_pool.get_connection() is not None

    def test_when_connection_builder_doesnt_work(self):
        with pytest.raises(DatabaseError) as ex:
            connection_pool = MySQLConnectionPoolBuilder.builder().port(3318).build()
        assert "Can't connect to MySQL server" in str(ex.value)