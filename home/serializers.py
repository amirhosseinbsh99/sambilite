from rest_framework import serializers
from home.models import Concert,Seat,Sans


class ConcertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Concert
        fields = "__all__"

class CreateConcertSerializer(serializers.ModelSerializer):
    co_image = serializers.ImageField(required=False)
    class Meta:
        model = Concert
        fields=['co_name','co_type','co_date','co_address','co_location','co_status','co_image','a_name','num_seats']

class ConcertImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Concert
        fields = ['co_image']


class ConcertDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concert
        fields = ['co_name', 'co_type', 'co_date', 'co_address', 'co_status', 'co_image']

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['from_seat','to_seat', 'se_row', 'se_area','se_price']

class CreateSeatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seat
        fields=['co_id','se_area','se_row','se_number','se_status','se_price','from_seat','to_seat']


class SansSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sans
        fields = "__all__"
class CreateSansSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sans
        fields ="__all__"

