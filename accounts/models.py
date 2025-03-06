
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from .validators import validate_phone_number


class Customer(AbstractUser):
    fullname = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    phone_number = models.CharField(
        max_length=11,
        validators=[validate_phone_number]
    )
    token_send = models.IntegerField(null=True, blank=True)
    last_otp_request = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    first_name = None
    last_name = None
    
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_admin = True
        else:
            self.username = self.phone_number
        super().save(*args, **kwargs)


@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance)
