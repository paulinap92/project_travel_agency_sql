from mysql.connector import pooling
from mysql.connector.pooling import MySQLConnectionPool
from typing import Self, Any
from dataclasses import field
import os
import logging

class MySQLConnectionPoolBuilder:
    """
    Builder class for constructing a MySQLConnectionPool instance with customizable configuration.

    This class follows the **Builder design pattern** to allow step-by-step construction of a `MySQLConnectionPool`
    with various parameters, enabling more flexible and readable code when initializing a connection pool.

    Attributes:
        _pool_config (dict): The configuration dictionary containing the parameters for the MySQL connection pool.

    Methods:
        pool_size: Sets the pool size of the connection pool.
        user: Sets the MySQL user for authentication.
        password: Sets the MySQL password for authentication.
        database: Sets the database to connect to.
        port: Sets the port for the MySQL server connection.
        build: Constructs and returns a `MySQLConnectionPool` instance with the provided configuration.
        builder: A class method to create a new instance of the builder.
    """

    def __init__(self, params: dict[str, Any] = None):
        """
        Initializes the builder with default parameters or custom ones provided in `params`.

        Args:
            params (dict, optional): A dictionary of parameters for the connection pool configuration.
                                      If not provided, default values will be used.

        Default configuration includes:
            - pool_name: 'my_pool'
            - pool_size: 5
            - host: 'localhost'
            - database: 'db_1'
            - user: 'user'
            - password: 'user1234'
            - port: 3307
        """
        params = {} if not params else params
        self._pool_config = {
            'pool_name': 'my_pool',
            'pool_size': 5,
            'host': 'localhost',
            'database': 'db_1',
            'user': 'user',
            'password': 'user1234',
            'port': 3307
        } | params

    def pool_size(self, new_pool_size: int) -> Self:
        """
        Sets the size of the connection pool.

        Args:
            new_pool_size (int): The new size of the connection pool.

        Returns:
            Self: The current `MySQLConnectionPoolBuilder` instance for method chaining.
        """
        self._pool_config['pool_size'] = new_pool_size
        return self

    def user(self, data: str) -> Self:
        """
        Sets the user for the MySQL connection.

        Args:
            data (str): The MySQL user name.

        Returns:
            Self: The current `MySQLConnectionPoolBuilder` instance for method chaining.
        """
        self._pool_config['user'] = data
        return self

    def password(self, data: str) -> Self:
        """
        Sets the password for the MySQL connection.

        Args:
            data (str): The MySQL password.

        Returns:
            Self: The current `MySQLConnectionPoolBuilder` instance for method chaining.
        """
        self._pool_config['password'] = data
        return self

    def database(self, data: str) -> Self:
        """
        Sets the database for the MySQL connection.

        Args:
            data (str): The name of the MySQL database.

        Returns:
            Self: The current `MySQLConnectionPoolBuilder` instance for method chaining.
        """
        self._pool_config['database'] = data
        return self

    def port(self, data: int) -> Self:
        """
        Sets the port for the MySQL connection.

        Args:
            data (int): The port number.

        Returns:
            Self: The current `MySQLConnectionPoolBuilder` instance for method chaining.
        """
        self._pool_config['port'] = data
        return self

    def build(self) -> MySQLConnectionPool:
        """
        Constructs and returns a `MySQLConnectionPool` instance with the configured parameters.

        Returns:
            MySQLConnectionPool: The constructed MySQL connection pool instance.
        """
        return MySQLConnectionPool(**self._pool_config)

    @classmethod
    def builder(cls) -> Self:
        """
        Creates and returns a new instance of the `MySQLConnectionPoolBuilder`.

        Returns:
            Self: A new instance of `MySQLConnectionPoolBuilder`.
        """
        return cls()

connection_pool = MySQLConnectionPoolBuilder.builder().port(3307).build()
