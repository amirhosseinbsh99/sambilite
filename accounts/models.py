
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Customer(AbstractUser):
    CustomerName = models.CharField(max_length=100)
    CustomerLocation = models.CharField(max_length=40)
    is_admin = models.BooleanField(default=False)

    first_name = None
    last_name = None
    

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance)