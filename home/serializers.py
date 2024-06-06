from rest_framework import serializers
from home.models import Concert,Seat,Sans,Rows,Slider
from django_jalali.serializers.serializerfield import JDateField, JDateTimeField

class RowsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rows
        fields = ['ConcertId', 'Rowid', 'RowNumber', 'RowPrice', 'RowArea', 'NumberofSeat', 'SansId']

class SansSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Sans
        fields = "__all__"

class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__' 

class CreateSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ['ConcertId','title','description','image','url']

class ConcertSerializer(serializers.ModelSerializer):
    Sans = SansSerializer(read_only=True, source='SansId')
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



class CreateSansSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sans
        fields =['ConcertId','SansTime','SansId','SansNumber','SansDate']

class GetRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rows
        fields="__all__"


class CreateSeatsSerializer(serializers.ModelSerializer):
    NumberofSeat = serializers.IntegerField(source='Rowid.NumberofSeat', read_only=True)
    RowNumber = serializers.IntegerField(read_only=True, source='Rowid.RowNumber')
    RowPrice = serializers.IntegerField(read_only=True, source='Rowid.RowPrice')
    RowArea = serializers.CharField(read_only=True, source='Rowid.RowArea')

    class Meta:
        model = Seat
        fields = ['NumberofSeat','ConcertId','Rowid', 'RowNumber','SeatNumber','SeatId','RowArea', 'RowPrice', 'SeatPrice']

  
    

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

class UpdateSansSerializer(serializers.ModelSerializer):
    SansDate = JDateField()
    class Meta:
        model = Sans
        fields = ['SansTime','SansDate']