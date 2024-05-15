from rest_framework import serializers
from home.models import Concert,Seat,Sans

class RowsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Concert
        fields = "__all__"


class ConcertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Concert
        fields = "__all__"

class CreateConcertSerializer(serializers.ModelSerializer):
    ConcertImage = serializers.ImageField(required=False)
    class Meta:
        model = Concert
        fields=['ConcertName','ConcertType','ConcertDate','ConcertAddress','ConcertLocation','NumberofRows','ConcertStatus','ConcertImage','ArtistName']

class ConcertImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Concert
        fields = ['ConcertName']


class ConcertDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concert
        fields = ['ConcertName', 'ConcertType', 'ConcertDate', 'ConcertAddress', 'ConcertStatus', 'ConcertImage']

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['SeatRow', 'SeatArea','SeatPrice']

class CreateSeatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seat
        fields=['ConcertId','SeatArea','SeatRow','se_status','SeatPrice']


class SansSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sans
        fields = "__all__"
class CreateSansSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sans
        fields ="__all__"

