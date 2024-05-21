from rest_framework import serializers
from home.models import Concert,Seat,Sans,Rows

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
        fields="__all__"


class ConcertImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Concert
        fields = ['ConcertName']


class ConcertDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concert
        fields = ['ConcertName', 'ConcertType', 'ConcertDate', 'ConcertAddress', 'ConcertStatus', 'ConcertImage']



class CreateRowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rows
        fields = ['ConcertId', 'RowNumber', 'NumberofSeat', 'RowPrice', 'RowArea']


class SansSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sans
        fields = "__all__"
class CreateSansSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sans
        fields ="__all__"

class GetRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rows
        fields = "__all__"


class CreateSeatsSerializer(serializers.ModelSerializer):
    Row = GetRowSerializer(read_only=True, source='Rowid')
    NumberofSeat = serializers.IntegerField(source='Rowid.NumberofSeat', read_only=True)

    RowNumber = serializers.IntegerField(read_only=True, source='Rowid.RowNumber')
    RowPrice = serializers.IntegerField(read_only=True, source='Rowid.RowPrice')
    RowArea = serializers.CharField(read_only=True, source='Rowid.RowArea')


    class Meta:
        model = Seat
        fields = ['Row', 'ConcertId', 'Rowid','RowNumber', 'NumberofSeat','RowArea','RowPrice','SeatPrice','SeatNumber']    

class SeatSerializer(serializers.ModelSerializer):
    Row = GetRowSerializer(read_only=True, source='Rowid')
    class Meta:
        model = Seat
        fields = ['Row','SeatId','SeatNumber','SeatPrice','SeatStatus']
        
class UpdateSeatSerializer(serializers.ModelSerializer):
    Row = GetRowSerializer(read_only=True, source='Rowid')
    class Meta:
        model = Seat
        fields = ['Row','SeatId','SeatPrice','SeatStatus']