from django.test import TestCase
from .models import Airport, Flight
# Create your tests here.


class ModelsTestCase(TestCase):

    def setUp(self):

        Air1 = Airport.objects.create( code="LAG", city = 'Lagos')
        Air2 = Airport.objects.create( code="OGN", city = 'Ogun')

        Flight.objects.create(origin=Air1, destination=Air2, duration=100)
        Flight.objects.create(origin=Air1, destination=Air1, duration=200)
        Flight.objects.create(origin=Air1, destination=Air2, duration=-100)


    def test_departure_count(self):

        a = Airport.objects.get(code="LAG")
        self.assertEqual(a.departures.count(), 3)


    def test_arrival_count(self):
        a = Airport.objects.get(code="LAG")
        self.assertEqual(a.arrivals.count(),1)

    def test_flight_valid(self):
        Air1 = Airport.objects.get(code="LAG")
        Air2 = Airport.objects.get(code="OGN")
        f = Flight.objects.get(origin = Air1, destination = Air2, duration=100)
        self.assertTrue(f.is_valid())

    def test_invalid_destination(self):

        Air = Airport.objects.get(code="LAG")
        f = Flight.objects.get(origin=Air, destination=Air)

        self.assertFalse(f.is_valid())

    def tes_invalid_duration(self):
        f = Flight.objects.get( duration = -100)

        self.assertFalse(f.is_valid())
