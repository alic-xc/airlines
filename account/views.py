from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return render(request, "account/login.html", {"message":None})

    context = {
        "user":request.user
    }
    return render(request, "account/user.html", )

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "account/login.html", {"message":"Invalid Username/ password"})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))
