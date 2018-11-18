from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import  Flight, Passenger

# Create your views here.
def index(request):
    #passing information inside the index.html file

    context = {
    "flights": Flight.objects.all()
    }
    return render(request, "flights/index.html", context)

def flight(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight Does Not Exist")

    context = {
    "flight":flight,
    "passengers": flight.passengers.all(),
    "non_passengers": Passenger.objects.exclude(flights=flight).all()
    }
    return render(request, "flights/flight.html", context)

def book(request, flight_id):
    try:
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
        flight = Flight.objects.get(pk=flight_id)

    except KeyError:
        return render( request, "flights/error", {"message":"No Selection"})

    except Passenger.DoesNotExist:
        return render( request, "flights/error", {"message":"No Passenger"})

    except Flight.DoesNotExist:
        return render( request, "flights/error", {"message":"No Flight"})

    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flight", args=(flight_id,)))
