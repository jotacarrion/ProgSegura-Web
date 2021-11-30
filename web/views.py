from django.shortcuts import render, redirect
# Login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as do_logout
from django.contrib.auth import login as do_login
from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from web.models import Product, ProfileUser

# Create your views here.


def login(request):
    context = {}

    if request and request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            do_login(request, user)
            request.session['username'] = username
            return redirect('index')

    return render(request, 'login.html', context)


@login_required
def logout(request):
    do_logout(request)
    return redirect('login')


@login_required
def error_profile(request):
    context = {}
    return render(request, 'error-perfil.html', context)


@login_required
def index(request):
    context = {}

    username = request.session.get('username')
    user = User.objects.get(username=username)
    context['user'] = user

    all_products = Product.objects.all()
    context['all_products'] = all_products

    if request.POST:
        if 'first_name' in request.POST and 'email' in request.POST:
            first_name = request.POST['first_name']
            email = request.POST['email']

            if 'phone' in request.POST and request.POST['phone']:
                phone = request.POST['phone']
                if not user_detail and phone:
                    ProfileUser.objects.create(username=user, phone_number=phone)
                else:
                    ProfileUser.objects.filter(username=user).update(phone_number=phone)
                return redirect('user-detail')

    return render(request, 'index.html', context=context)


@login_required
def user_detail(request, user_id):
    context = {}
    if User.objects.filter(id=user_id).exists():
        user = User.objects.get(id=user_id)
        if user.username == request.session.get('username'):
            context['user'] = user

            username = user.username
            user_detail = None

            if ProfileUser.objects.filter(username=user).exists():
                user_detail = ProfileUser.objects.get(username=user)

            if request.FILES:
                if 'image_profile' in request.FILES and request.FILES['image_profile']:
                    if ProfileUser.objects.filter(username=user).exists():
                        profile_user_viewing = ProfileUser.objects.get(username=user)
                    else:
                        profile_user_viewing = ProfileUser.objects.create(username=user, phone_number=None, image_profile=None)
                    profile_user_viewing.image_profile = request.FILES['image_profile']
                    profile_user_viewing.save()


            if request.POST:
                if 'first_name' in request.POST and 'last_name' in request.POST:
                    first_name = request.POST['first_name']
                    last_name = request.POST['last_name']
                    phone = None

                    User.objects.filter(username=username).update(first_name=first_name, last_name=last_name)
                    if 'phone' in request.POST and request.POST['phone']:
                        phone = request.POST['phone']
                        if not user_detail and phone:
                            ProfileUser.objects.create(username=user, phone_number=phone)
                        else:
                            ProfileUser.objects.filter(username=user).update(phone_number=phone)
                        return redirect('user-detail')

            context['user_detail'] = user_detail
            redirect('user-detail', user.id)
        else:
            return render(request, 'error-perfil.html', context=context)

    return render(request, 'user-detail.html', context=context)




@login_required
def product_update(request, product_id):
    context = {}

    username = request.session.get('username')
    user = User.objects.get(username=username)
    if ProfileUser.objects.filter(username=user).exists() and ProfileUser.objects.get(username=user).rol('admin'):

        if Product.objects.filter(id=product_id).exists():
            product = Product.objects.get(id=product_id)
            context['product'] = product

            if request.FILES:
                if 'image_product' in request.FILES and request.FILES['image_product']:
                    product.image_product = request.FILES['image_product']
                    product.save()

            if request.POST:
                if 'name' in request.POST and 'name' in request.POST:
                    name = request.POST['name']
                    description = request.POST['description']
                    price = request.POST['price']

                    Product.objects.filter(id=product_id).update(name=name, description=description, price=price)
                return redirect('product-update', product_id)

        return render(request, 'product-update.html', context=context)
    else:
        return render(request, 'error.html', context=context)
