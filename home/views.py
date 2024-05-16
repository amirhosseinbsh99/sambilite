from rest_framework.response import Response
from .models import Concert,Seat,Sans,Rows
from accounts.models import Customer
from rest_framework import generics
from .serializers import ConcertSerializer,CreateConcertSerializer,RowsSerializer,SeatSerializer,CreateSansSerializer,ConcertDetailSerializer,CreateSeatsSerializer,SansSerializer
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
import requests
import json
from django.http import request
from rest_framework.permissions import IsAuthenticated

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
        concerts = Concert.objects.filter(ConcertLocation=city)
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
    search_fields = ['$ArtistName']


    # def put(self, request, id):


        

    #     concert_obj = Concert.objects.get(ConcertId=id)       
    #     serializer = ConcertImageSerializer(instance=concert_obj, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     # Return the updated concert data
    #     return Response(serializer.data)
    


     ##* for admin *##
class ConcertAdminView(APIView):
   # permission_classes=(IsAuthenticated,)
    
    def create_rows(self, id, num_rows, row_price=None):
        try:
            concert = Concert.objects.get(ConcertId=id)

            rows = []

            for row_number in range(1, num_rows + 1):
                row = Rows(ConcertId=id, RowNumber=row_number, RowPrice=row_price)
                row.save()
                rows.append(row)
                print(row_number)

            return rows, None
        except Concert.DoesNotExist:
            return None, 'Concert not found.'

    def post(self, request):
        
        serializer = CreateConcertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        concert = serializer.save()  # Save the concert object and obtain its ID
        ConcertId = concert.ConcertId # Obtain the concert ID
          
        print(ConcertId)
        num_rows = request.data.get('NumberofRows', 0)
        row_price = request.data.get('rowprice')

        # Create rows for the concert
        if num_rows > 0:
            rows, error = self.create_rows(ConcertId, num_rows, row_price)
            if error:
                return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

            serializer = RowsSerializer(rows, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'تعداد ردیف.'}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, id=None):  
        if id is not None:
        
            concert = Concert.objects.get(ConcertId=id)
            serializer = ConcertSerializer(concert)
            return Response(serializer.data)
        else:
            # List all concerts
            all_concerts = Concert.objects.all()
            serializer = ConcertSerializer(all_concerts, many=True)
            return Response(serializer.data)

    

    def put(self, request, id):
        
        # Retrieve the concert object to update
        concert_obj = Concert.objects.get(ConcertId=id)
        
        # Update the concert object with the request data
        serializer = CreateConcertSerializer(instance=concert_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Return the updated concert data
        return Response(serializer.data)


    def delete(self,request,id):
        concerts_obj = Concert.objects.get(ConcertId=id)
        concerts_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class GenerateSeats(APIView):
    permission_classes=(IsAuthenticated,)


    def get(self, request, start, end,  id,row_id):
        try:
            concert_obj  = Concert.objects.get(pk=id)
            row_obj  = Rows.objects.get(pk=id)
            start = int(start)
            end = int(end)
            seats = []

            for SeatNumber in range(start, end + 1):
                seat = Seat(Concert=concert_obj,Rows=row_obj, SeatNumber=SeatNumber)
                seat.save()
                seats.append(seat)

            serializer = SeatSerializer(seats, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Concert.DoesNotExist:
            return Response({'error': 'Concert not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Rows.DoesNotExist:
            return Response({'error': 'Row not found.'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({'error': 'Invalid input. Please provide integers for start and end.'}, status=status.HTTP_400_BAD_REQUEST)
#if seat status changed change its icon to other color it means change its icon
class ConcertDetail(APIView):
    # def get(self, request, ConcertId):
    #     try:
    #         concert = Concert.objects.get(pk=ConcertId)
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
        ConcertId = serializer.validated_data.get('ConcertId')
        
        if Seat.objects.filter(ConcertId=ConcertId).exists():
            return Response({"message": "تکراری بودن صندلی ها"}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
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
        seat_obj = Seat.objects.get(ConcertId=id)



        # Update the seat object with the request data
        serializer = CreateSeatsSerializer(instance=seat_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        

class SelectSeat(APIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer





class SansAdminView(APIView):

    def post(self,request):
        serializer = CreateSansSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        SansNumber = serializer.validated_data.get('SansNumber')
        ConcertId = serializer.validated_data.get('ConcertId')
        print(ConcertId)
        SansTime = serializer.validated_data.get('SansTime')
        SansId = serializer.validated_data.get('SansId')
        if Sans.objects.filter(SansId=SansId).exists():
            return Response({"message": "این سانس از قبل ثبت شده است"}, status=status.HTTP_400_BAD_REQUEST)
        elif Sans.objects.filter(SansNumber=SansNumber, ConcertId=ConcertId, SansTime=SansTime).exists():
            return Response({"message": "این سانس تکراری است"}, status=status.HTTP_400_BAD_REQUEST)
        elif Sans.objects.filter(SansTime=SansTime,ConcertId=ConcertId).exists():
            return Response({"message": "تکراری بودن زمان سانس"}, status=status.HTTP_400_BAD_REQUEST)
        elif Sans.objects.filter(SansNumber=SansNumber,ConcertId=ConcertId).exists():
            return Response({"message": f"سانس {SansNumber} وجود دارد"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

    def get(self, request, id=None):
        if id is not None:

            seat = Sans.objects.get(se_id=id)
            serializer = CreateSansSerializer(seat)
            return Response(serializer.data)
        else:
            # List all concerts
            all_concerts = Sans.objects.all()
            serializer = CreateSansSerializer(all_concerts, many=True)
            return Response(serializer.data)



    def put(self, request, id):
        # Retrieve the seat object to update
        Sans_obj = Sans.objects.get(ConcertId=id)



        # Update the seat object with the request data
        serializer = CreateSansSerializer(instance=Sans_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

# class MakePayment(self,Serializer):

#     #serializer_class = PaymentSerializer
        
#     def perform_create(self, serializer):
#         # Assuming you have implemented a payment gateway integration
#         # Here you would process the payment and update the seat status to 'Selected'
#         serializer.save(customer=self.request.user)





        

    

    