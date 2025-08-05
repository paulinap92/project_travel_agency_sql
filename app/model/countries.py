from typing import Self
from dataclasses import dataclass
from app.file_manager.file_manager import FileManager
import re


@dataclass
class Country:
    """
    A class representing a country with its name and a validation pattern.

    Attributes:
        name (str): The name of the country.
        pattern (str): A regular expression pattern for validating country names. Defaults to `'^[A-Za-z ]+$'`.

    Methods:
        __repr__: Returns a string representation of the Country object.
        from_text: Class method to create a Country object from a string, validating the input data.
    """

    name: str
    pattern: str = r'^[A-Za-z ]+$'

    def __repr__(self) -> str: # pragma: no cover
        """
        Returns a string representation of the Country object.

        Returns:
            str: A string in the format of "Country(name=<country_name>)".
        """
        return f"Country(name={self.name})"

    @classmethod
    def from_text(cls, data: str) -> Self:
        """
        Creates a Country object from a string, validating the input data.

        Args:
            data (str): The country name to be validated and converted into a Country object.

        Raises:
            AttributeError: If the provided data does not match the pattern.

        Returns:
            Country: The created Country object.
        """
        if not re.match(cls.pattern, data):
            raise AttributeError(f'Data is not correct: {data}')

        return Country(data)


class CountryConverter:
    """
    A utility class for converting a list of country names to a dictionary of Country objects.

    Methods:
        to_countries: Converts a list of country names into a dictionary of Country objects, indexed by an integer.
    """

    @staticmethod
    def to_countries(data: list[str]) -> dict[int, Country]:
        """
        Converts a list of country names into a dictionary of Country objects.

        Args:
            data (list[str]): A list of country names to be converted.

        Returns:
            dict[int, Country]: A dictionary where the keys are integers (country IDs) and the values are Country objects.
        """
        countries: dict[int, Country] = {}
        id_ = 0
        for line in data:
            country = Country.from_text(line)
            countries.update({id_: country})
            id_ += 1
        return countries


class CountryRepo:
    """
    A repository class for storing and managing a collection of Country objects.

    Attributes:
        countries (dict[int, Country]): A dictionary of Country objects, indexed by country ID.

    Methods:
        __init__: Initializes the repository and optionally loads country data from a file.
        get_countries: Returns a list of country names stored in the repository.
    """

    countries: dict[int, Country]

    def __init__(self, path: str = None):
        """
        Initializes the CountryRepo with an optional path to a file containing country data.

        Args:
            path (str, optional): The file path to read country names from. Defaults to None.
        """
        if path:
            self.countries = CountryConverter.to_countries(FileManager(['read']).read_file(path))

    def get_countries(self) -> set[str]:
        """
        Retrieves a set of country names from the repository.

        Returns:
            set[str]: A set of country names.
        """
        return set([country.name for country in self.countries.values()])


european_countries_repo = CountryRepo('.\\app\\data\\european_countries.txt')
