from dataclasses import dataclass
from decimal import Decimal

# --------------------------------------------------
# ENTITIES
# --------------------------------------------------

@dataclass(frozen=True)
class Trip:
    """Represents a travel trip with destination, price, and other metadata.

    Attributes:
        _id (int | None): Unique identifier of the trip.
        _destination (str | None): Destination of the trip.
        _price (Decimal | None): Price of the trip per person.
        _num_of_people (int | None): Number of people in the trip.
        _agency_id (int | None): Identifier of the travel agency organizing the trip.
    """
    _id: int | None = None
    _destination: str | None = None
    _price: Decimal | None = 0
    _num_of_people: int | None = None
    _agency_id: int | None = None

    @property
    def id(self) -> int | None:
        """Returns the trip ID."""
        return self._id

    @property
    def destination(self) -> str | None:
        """Returns the destination of the trip."""
        return self._destination

    @property
    def price(self) -> Decimal | None:
        """Returns the price of the trip per person."""
        return self._price

    @property
    def num_of_people(self) -> int | None:
        """Returns the number of people for the trip."""
        return self._num_of_people

    @property
    def agency_id(self) -> int | None:
        """Returns the ID of the travel agency."""
        return self._agency_id

    def get_income(self, vat_rate: Decimal = Decimal('0.19'), margin: Decimal = Decimal('0.1')) -> Decimal:
        """Calculates the agency's income from the trip.

        Args:
            vat_rate (Decimal): Value-added tax rate applied to the price. Default is 0.19 (19%).
            margin (Decimal): Agency's margin rate. Default is 0.1 (10%).

        Returns:
            Decimal: The calculated income from the trip.

        Raises:
            TypeError: If the price is not set.
        """
        if self.price is None:
            raise TypeError("Price must be set to calculate income.")
        return self.price * vat_rate * margin
