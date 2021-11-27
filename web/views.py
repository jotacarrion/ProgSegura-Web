from django.shortcuts import render, redirect
# Login
from django.contrib.auth import login as do_login
from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from web.models import ProfileUser

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


#@login_required
#def user_detail(request, user_id):
def user_detail(request):
    context = {}
    user_id = 1
    if User.objects.filter(id=user_id).exists():

        user = User.objects.get(id=user_id)

        username = user.username
        context['user_detail'] = None
        user_detail = None
        if ProfileUser.objects.filter(username=user).exists():
            user_detail = ProfileUser.objects.get(username=user)
            context['user_detail'] = user_detail

        if request.POST:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']

            User.objects.filter(username=username).update(first_name=first_name, last_name=last_name)
            if 'phone' in request.POST and request.POST['phone']:
                phone = request.POST['phone']
                if not user_detail and phone:
                    ProfileUser.objects.create(username=user, phone_number=phone)
                else:
                    ProfileUser.objects.filter(username=user).update(phone_number=phone)
                return redirect('user-detail')

    return render(request, 'user-detail.html', context=context)
