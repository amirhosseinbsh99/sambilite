from rest_framework import serializers
from home.models import Concert, Seat, Sans, Rows, Slider, Order, OrderItem
from accounts.models import Customer


class RowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rows
        fields = ['concert', 'row_number', 'row_price', 'row_area', 'number_of_seat', 'sans']


class SansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sans
        fields = '__all__'


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'


class CreateSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ['title', 'description', 'image', 'url']


class ConcertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concert
        fields = '__all__'


class CreateConcertSerializer(serializers.ModelSerializer):
    concert_image = serializers.ImageField(required=False)

    class Meta:
        model = Concert
        fields = '__all__'


class ConcertImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concert
        fields = ['concert_name']


class ConcertDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concert
        fields = ['concert_name', 'concert_type', 'concert_date', 'concert_address', 'concert_status', 'concert_image']


class CreateRowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rows
        fields = ['concert', 'row_number', 'number_of_seat', 'row_price', 'row_area']


class CreateSansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sans
        fields = ['concert', 'sans_time', 'sans_number', 'sans_date', 'sans_status']


class GetRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rows
        fields = '__all__'


class CreateSeatsSerializer(serializers.ModelSerializer):
    number_of_seat = serializers.IntegerField(source='row.number_of_seat', read_only=True)
    row_number = serializers.IntegerField(read_only=True, source='row.row_number')
    row_price = serializers.IntegerField(read_only=True, source='row.row_price')
    row_area = serializers.CharField(read_only=True, source='row.row_area')

    class Meta:
        model = Seat
        fields = ['number_of_seat', 'concert', 'row', 'row_number', 'seat_number', 'row_area', 'row_price', 'seat_price', 'seat_status']


class SeatSerializer(serializers.ModelSerializer):
    row = GetRowSerializer(read_only=True, source='row')

    class Meta:
        model = Seat
        fields = ['row', 'seat_number', 'seat_price', 'seat_status']


class UpdateSeatSerializer(serializers.ModelSerializer):
    row = GetRowSerializer(read_only=True, source='row')

    class Meta:
        model = Seat
        fields = ['row', 'seat_price', 'seat_status']


class UpdateSansSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sans
        fields = ['sans_time', 'sans_date']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
