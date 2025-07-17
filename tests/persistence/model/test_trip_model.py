from app.persistence.model import Trip
from decimal import Decimal
import pytest

class TestTripModel:
    def test_when_trip_model_is_created_correct(self):
        trip_id = 1
        destination = 'Poland'
        price = Decimal('0.13')
        num_of_people = 12
        agency_id = 5

        trip = Trip(_id = trip_id, _destination=destination, _price=price, _num_of_people=num_of_people,
                    _agency_id=agency_id)

        assert ((trip_id, destination, price, num_of_people, agency_id) ==
                (trip.id, trip.destination, trip.price, trip.num_of_people, trip.agency_id))

    def test_get_income_with_custom_rates(self):
        trip = Trip(_price=Decimal('1000.00'))
        income = trip.get_income(vat_rate=Decimal('0.20'), margin=Decimal('0.15'))
        assert income == Decimal('1000.00') * Decimal('0.20') * Decimal('0.15')

    def test_get_income_raises_type_error_if_price_none(self):
         trip = Trip(_price=None)
         with pytest.raises(TypeError) as exc_info:
             trip.get_income()

         assert str(exc_info.value) == "Price must be set to calculate income."

