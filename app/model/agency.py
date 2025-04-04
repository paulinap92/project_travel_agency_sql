from typing import Self
from dataclasses import dataclass
from app.file_manager.file_manager import FileManager
import re


@dataclass(frozen=True)
class Agency:
    """Represents a travel agency.

    Attributes:
        _id (int): Agency identifier.
        _name (str): Agency name.
        _localization (str): Agency location.
        pattern (str): Regular expression pattern for input data validation.
    """
    _id: int
    _name: str
    _localization: str
    pattern: str = r'^\d+,[A-Za-z ]+,[A-Za-ęóąśłżźćń ]+$'

    def __repr__(self) -> str:  # pragma: no cover
        """Returns a string representation of the Agency object."""
        return f"Agency(id_={self._id}, name={self._name}, localization={self._localization})"

    @property
    def id(self) -> int:
        """Returns the agency identifier."""
        return self._id

    @property
    def name(self) -> str:  # pragma: no cover
        """Returns the agency name."""
        return self._name

    @classmethod
    def from_text(cls, data: str) -> Self:
        """Creates an Agency object from a text string.

        Args:
            data (str): A string containing agency data in the format "id,name,location".

        Returns:
            Agency: An Agency object created from the input data.

        Raises:
            AttributeError: If the input data format does not match the expected pattern.
        """
        if not re.match(cls.pattern, data):
            raise AttributeError(f'Invalid data: {data}')
        items = data.split(',')
        return Agency(int(items[0]), items[1], items[2])


class AgencyConverter:
    """Class for converting text data into Agency objects."""

    @staticmethod
    def to_agencies(data: list[str]) -> dict[int, Agency]:
        """Converts a list of text data into a dictionary of Agency objects.

        Args:
            data (list[str]): A list of strings containing agency data.

        Returns:
            dict[int, Agency]: A dictionary where the key is the agency ID and the value is an Agency object.
        """
        agencies: dict[int, Agency] = {}
        for line in data:
            agency = Agency.from_text(line)
            agencies.update({agency.id: agency})
        return agencies


class AgencyRepo:
    """Repository for managing agency data."""
    agencies: dict[int, Agency]

    def __init__(self, path: str | None = None):
        """Initializes the agency repository.

        Args:
            path (str | None): Path to the file containing agency data.
        """
        if path:
            self.agencies = AgencyConverter.to_agencies(FileManager(['read']).read_file(path))

    def get_agencies(self) -> list[Agency]:
        """Returns a list of all agencies.

        Returns:
            list[Agency]: A list of Agency objects.
        """
        return list(self.agencies.values())

    def get_by_id(self, agency_id: int) -> Agency:
        """Returns an agency based on its identifier.

        Args:
            agency_id (int): Agency identifier.

        Returns:
            Agency: The Agency object with the specified ID, or None if not found.
        """
        return self.agencies.get(agency_id)

    def agency_name_for_id(self, agency_id: int) -> str:
        """Returns the agency name based on its identifier.

        Args:
            agency_id (int): Agency identifier.

        Returns:
            str: The agency name or 'Unknown agency' if the agency does not exist.
        """
        return self.agencies.get(agency_id, 'Unknown agency').name


agency_repo = AgencyRepo('.\\app\\data\\travel_agency.txt')