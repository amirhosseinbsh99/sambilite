from rest_framework import serializers
from home.models import Concert,Customer


class ConcertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Concert
        fields = "__all__"
# important for creating concert
class CreateConcertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concert
        fields=['co_name','co_type','co_date','co_address','co_seats','co_status','co_image','a_name']


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = "__all__"

class CreateCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields=['cu_name','cu_phonenumber','cu_email']




