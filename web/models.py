from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class ProfileUser(models.Model):
    rol_choices = (
        ('admin', 'Empleado'),
        ('user', 'Usuario'),
    )
    phone_number = models.CharField(max_length=16)
    rol = models.CharField(max_length=12, choices=rol_choices , blank=True, null=True)
    image_profile = models.ImageField(upload_to='users/image_profiles', default=True, blank=True, null=True)
    username = models.OneToOneField(User, models.DO_NOTHING, unique=True)
#    is_active = models.IntegerField()

    def __unicode__(self, ):
        return str(self.phone_number)

class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    image_product = models.ImageField(upload_to='products', default=True, blank=True, null=True)
    price = models.FloatField()
