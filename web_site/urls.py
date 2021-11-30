"""web_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from web import views
from web_site import settings

urlpatterns = [
    #path('user-detail/?P<username>\w+)/$', views.user_detail, name='user-detail'),
    path('user-detail/<int:user_id>/', views.user_detail, name='user-detail'),
    path('product-update/<int:product_id>/', views.product_update, name='product-update'),
    #path('products', views.products, name='products'),
    path('', views.index, name='index'),
    path('error', views.error_profile, name='error-profile'),
    path('admin/', admin.site.urls),

    #path('user-detail', views.user_detail, name='user-detail'),

    path('login', views.login, name='login'),
] + static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
