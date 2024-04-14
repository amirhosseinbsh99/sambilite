
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import AbstractUser



class Customer(AbstractUser):
    cu_id = models.AutoField(primary_key=True)
    cu_name = models.CharField(max_length=100)
    cu_phonenumber = models.CharField(max_length=11, unique=True)
    cu_location = models.CharField(max_length=40)

    USERNAME_FIELD = 'cu_phonenumber'
    first_name = None
    last_name = None
    


    def __str__(self):
        return self.cu_phonenumber  # Customize the string representation of the user object

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance)