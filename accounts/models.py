from django.db import models
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.utils import timezone


# Create your models here.


class Customer(models.Model):
    cu_id = models.AutoField(primary_key=True)
    cu_name = models.CharField(max_length=100)
    cu_phonenumber = models.CharField(max_length=11)
    cu_email = models.EmailField(max_length=254 ,blank=True)
    cu_location = models.CharField(max_length=40)
    cu_password = models.CharField(max_length=128)



class CustomToken(Token):
    """
    Extend Django Rest Framework's Token model to add additional fields or methods if needed.
    """
    # Add additional fields or methods if needed
    created = models.DateTimeField(default=timezone.now)