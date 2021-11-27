from django.shortcuts import render, redirect
# Login
from django.contrib.auth import login as do_login
from django.contrib.auth import authenticate

# Create your views here.

def login(request):
    context = {}

    if request and request.POST:
        print('-request.POST', request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            do_login(request, user)
            return redirect('index')

    return render(request, 'login.html', context)


def index(request):
    context = {}

    return render(request, 'index.html', context=context)