from rest_framework import serializers
from home.models import Concert,Customer


class ConcertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Concert
        fields = "__all__"

class CreateConcertSerializer(serializers.ModelSerializer):
    co_image = serializers.ImageField(required=False)
    class Meta:
        model = Concert
        fields=['co_name','co_type','co_date','co_address','co_seats','co_status','co_image','a_name']







