from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class ProfileUser(models.Model):
    phone_number = models.CharField(max_length=16)
    image_profile = models.ImageField(upload_to='users/image_profiles', default=True, blank=True, null=True)
    visible = models.IntegerField()
    upload_at = models.DateTimeField(blank=True, null=True)
    username = models.CharField(unique=True, max_length=150)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()

    def get_user(self):
        return User.objects.get(username=self.username)


class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    price = models.FloatField()
