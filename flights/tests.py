from django.db.models import Max
from django.test import Client, TestCase

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
        f = Flight.objects.get(origin = Air1, destination = Air2, duration=100`)
        self.assertTrue(f.is_valid())

    def test_invalid_destination(self):

        Air = Airport.objects.get(code="LAG")
        f = Flight.objects.get(origin=Air, destination=Air)

        self.assertFalse(f.is_valid())

    def tes_invalid_duration(self):
        f = Flight.objects.get( duration = -100)

        self.assertFalse(f.is_valid())

    def test_index(self):
        c = Client()
        response = c.get("/")
        self.assertEqual( response.status_code, 200 )
        self.assertEqual( response.context["flights"].count, 2)

    def test_valid_flight(self):

         a1 = Airport.objects.get(code='LAG')
         f = Flight.objects.get(origin=a1, destination= a1)
         c  = Client()

         response = c.get(f'/{ f.id }')
         self. assertEqual( response.status_code, 200)


    def test_flight_invalid(self):

        max_id = Flight.objects.all().aggregrate( Max("id"))["id__max"]

        c = Client()
        response = c.get(f"/{max_id + 1 }")

        self.assertEqual(response.status_code, 404)


    def test_flight_passenger(self):

        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="olamilekan", last="ismail")
        f.passengers.add(p)

        c = Client()
        response = c.get(f"/{f.id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['passengers'].count(), 1)

    def test_flight_non_passenger(self):

        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="olamilekan O", last=" P ismail")

        c = Client()

        response = c.get(f"/{f.id}")

        self.assertEqual( response.status_code, 200)
        self.assertEqual(response.context['passengers'].count(), 1)
