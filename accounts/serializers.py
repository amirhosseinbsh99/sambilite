from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['cu_id', 'cu_name', 'cu_phonenumber', 'cu_email', 'cu_location']


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = "__all__"

class CreateCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields=['cu_name','cu_phonenumber','cu_email','cu_location']