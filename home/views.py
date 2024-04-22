from rest_framework.response import Response
from .models import Concert,Seat,Sans
from accounts.models import Customer
from .serializers import ConcertSerializer,CreateConcertSerializer,SeatSerializer,ConcertDetailSerializer,CreateSeatsSerializer,SansSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework import viewsets
from django.utils import timezone
from datetime import timedelta,datetime
from rest_framework import filters  
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
import requests,base64
import json
from django.http import request


#for updating put
#from rest_framework.parsers import MultiPartParse

viewsets.ModelViewSet

#generic views
class ListConcertView(ListAPIView):

    def get(self, request):
        ip_response = requests.get('https://api.ipify.org/?format=json')
        ip_data = ip_response.json()
        myip = ip_data.get('ip')
               
        location_response = requests.get(f'http://ip-api.com/json/{myip}')
        location_data = location_response.json()
        city = location_data.get('city')


   # Filter concerts based on the city
        concerts = Concert.objects.filter(co_location=city)
        if not concerts.exists():
            # If no concerts found, fetch all concerts
            concerts = Concert.objects.all()

        # Serialize the filtered concerts
        serializer = ConcertSerializer(concerts, many=True)

        return Response(serializer.data)
    # def get(self, request):
    #     res = requests.get('http://ip-api.com/json/46.182.32.18')  # Send request to IP API
    #     location_data = res.json() # Extract JSON data from response
    #     city = location_data.get('city')  # Extract city from location data
    #     return Response({'city': city})

    serializer_class = ConcertSerializer
   # parser_classes = [MultiPartParser]
    def get_queryset(self):
        timeframe = self.request.query_params.get('timeframe')

        if timeframe == 'forever':
            return Concert.objects.all()
        elif timeframe == 'last_of_this_week':
            return self.get_last_of_this_week_concerts()
        elif timeframe == 'this_week':
            return self.get_this_week_concerts()
        elif timeframe == 'this_month':
            return self.get_this_month_concerts()
        elif timeframe == 'next_week':
            return self.get_next_week_concerts()
        elif timeframe == 'next_month':
            return self.get_next_month_concerts()
        else:
            return Concert.objects.all()

    def get_last_of_this_week_concerts(self):
        today = timezone.now().date()
        last_of_this_week = today + timedelta(days=6 - today.weekday())
        return Concert.objects.filter(co_date__lte=last_of_this_week)

    def get_this_week_concerts(self):
        today = timezone.now().date()
        end_of_this_week = today + timedelta(days=6 - today.weekday())
        start_of_this_week = end_of_this_week - timedelta(days=6)
        return Concert.objects.filter(co_date__range=[start_of_this_week, end_of_this_week])

    def get_this_month_concerts(self):
        today = timezone.now().date()
        start_of_this_month = datetime(today.year, today.month, 1).date()
        end_of_this_month = datetime(today.year, today.month + 1, 1).date() - timedelta(days=1)
        return Concert.objects.filter(co_date__range=[start_of_this_month, end_of_this_month])

    def get_next_week_concerts(self):
        today = timezone.now().date()
        start_of_next_week = today + timedelta(days=(7 - today.weekday()) + 1)
        end_of_next_week = start_of_next_week + timedelta(days=6)
        return Concert.objects.filter(co_date__range=[start_of_next_week, end_of_next_week])

    def get_next_month_concerts(self):
        today = timezone.now().date()
        start_of_next_month = datetime(today.year, today.month + 1, 1).date()
        end_of_next_month = datetime(today.year, today.month + 2, 1).date() - timedelta(days=1)
        return Concert.objects.filter(co_date__range=[start_of_next_month, end_of_next_month])
    

class ConcertSearchView(ListAPIView):

    queryset = Concert.objects.all()
    serializer_class = ConcertSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['$a_name']

class CreateListConcertView(CreateAPIView):
    queryset = Concert.objects.all()
    serializer_class = CreateConcertSerializer
    def perform_create(self, serializer):
        # Extract the uploaded image from the request data
        image_file = self.request.data.get('co_image')

        if image_file:
            # Read the image file into memory
            image_data = image_file.read()

            # Encode the image data into base64
            base64_image = base64.b64encode(image_data).decode('utf-8')

            # Replace the original image data with the base64 encoded string
            self.request.data['co_image'] = base64_image

        # Call the serializer's save method with the modified request data
        serializer.save()
#class base
     ##* for admin *##
class ConcertAdminView(APIView):
    #if user is authendicated user can see the concerts else it will return permission denied error message
    #permission_classes=(IsAuthenticated,)


    def post(self,request):
        serializer = CreateConcertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def get(self, request, id=None):  
        if id is not None:
        
            concert = Concert.objects.get(co_id=id)
            serializer = ConcertSerializer(concert)
            return Response(serializer.data)
        else:
            # List all concerts
            all_concerts = Concert.objects.all()
            serializer = ConcertSerializer(all_concerts, many=True)
            return Response(serializer.data)



    def put(self, request, id):
        # Retrieve the concert object to update
        concert_obj = Concert.objects.get(co_id=id)

        # Check if the request contains image data
        image_data = request.data.get('co_image')

        if image_data:
            # Decode the base64 encoded image data
            try:
                decoded_image = base64.b64decode(image_data)
            except Exception as e:
                return Response({"error": "Invalid base64 encoded image data"}, status=status.HTTP_400_BAD_REQUEST)

            # Update the concert object with the new image data
            request.data['co_image'] = decoded_image

        # Update the concert object with the request data
        serializer = CreateConcertSerializer(instance=concert_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Return the updated concert data
        return Response(serializer.data)


    def delete(self,request,id):
        concerts_obj = Concert.objects.get(co_id=id)
        concerts_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ConcertDetail(APIView):
    # def get(self, request, co_id):
    #     try:
           
    #         concert = Concert.objects.get(pk=co_id)
    #         serializer = ConcertSerializer(concert)
    #         return Response(serializer.data)
    #     except Concert.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    def get(self,request,id):
        concerts = Concert.objects.all()
        seats = Seat.objects.all()
        sans = Sans.objects.all()

        concert_serializer = ConcertSerializer(concerts, many=True)
        seat_serializer = SeatSerializer(seats, many=True)
        sans_serializer = SansSerializer(sans, many=True)

        return Response({
        'concerts': concert_serializer.data,
        'seats': seat_serializer.data,
        'sans' : sans_serializer.data
    }, status=status.HTTP_200_OK)


class SeatsAdminView(APIView):

    def post(self,request):
        serializer = CreateSeatsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def get(self, request, id=None):
        if id is not None:

            seat = Seat.objects.get(se_id=id)
            serializer = CreateSeatsSerializer(seat)
            return Response(serializer.data)
        else:
            # List all concerts
            all_concerts = Seat.objects.all()
            serializer = CreateSeatsSerializer(all_concerts, many=True)
            return Response(serializer.data)



    def put(self, request, id):
        # Retrieve the seat object to update
        seat_obj = Seat.objects.get(co_id=id)



        # Update the seat object with the request data
        serializer = CreateSeatsSerializer(instance=seat_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        
        








        

    

    