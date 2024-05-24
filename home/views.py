from rest_framework.response import Response
from .models import Concert,Seat,Sans,Rows
from accounts.models import Customer
from rest_framework import generics
from .serializers import ConcertSerializer,CreateConcertSerializer,SeatSerializer,UpdateSeatSerializer,CreateSansSerializer,CreateSeatsSerializer,SansSerializer,GetRowSerializer,UpdateSansSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,UpdateAPIView
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
    def post(self, request):
        data = request.data
        serializer = CreateConcertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        concert = serializer.save()

        number_of_Sans = concert.NumberofSans
        number_of_rows = concert.NumberofRows

        Sans_to_create = [
            Sans(ConcertId=concert, SansNumber=i+1)
            for i in range(number_of_Sans)
        ]
        Sans.objects.bulk_create(Sans_to_create)

        # Create Rows for each Sans
        for sans in Sans.objects.filter(ConcertId=concert):
            rows_to_create = [
                Rows(ConcertId=concert, SansId=sans, RowNumber=i+1)
                for i in range(number_of_rows)
            ]
            Rows.objects.bulk_create(rows_to_create)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, id=None):
        if id is not None:
            try:
                concert = Concert.objects.get(ConcertId=id)
                serializer = ConcertSerializer(concert)
                return Response({
                    'concerts': serializer.data,
                }, status=status.HTTP_200_OK)
            except Concert.DoesNotExist:
                return Response({'error': 'Concert not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # List all concerts
            all_concerts = Concert.objects.all()
            serializer = ConcertSerializer(all_concerts, many=True)
            return Response({
                'concerts': serializer.data,
            }, status=status.HTTP_200_OK)

    def put(self, request, id):
        try:
            # Retrieve the concert object to update
            concert_obj = Concert.objects.get(ConcertId=id)
            old_number_of_Sans = concert_obj.NumberofSans
            
            # Update the concert object with the request data
            serializer = CreateConcertSerializer(instance=concert_obj, data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_concert = serializer.save()

            # Update the rows for the updated concert
            current_number_of_rows = updated_concert.NumberofRows
            existing_rows = Rows.objects.filter(ConcertId=updated_concert)
            existing_rows_count = existing_rows.count()
            
            if existing_rows_count != current_number_of_rows:
                # Delete the existing rows
                existing_rows.delete()
                

                # Create Rows for each Sans
            for sans in Sans.objects.filter(ConcertId=updated_concert):
                rows_to_create = [
                    Rows(ConcertId=updated_concert, SansId=sans, RowNumber=i+1)
                    for i in range(current_number_of_rows)
                ]
                Rows.objects.bulk_create(rows_to_create)

            # Update the Sans if the NumberofSans has changed
            new_number_of_Sans = updated_concert.NumberofSans
            if old_number_of_Sans != new_number_of_Sans:
                # Delete existing Sans and their rows
                Sans.objects.filter(ConcertId=updated_concert).delete()
                
                # Create new Sans individually
                for i in range(new_number_of_Sans):
                    new_sans = Sans(ConcertId=updated_concert, SansNumber=i+1)
                    new_sans.save()
                
                # Query the database to get the newly created Sans with their primary keys
                new_sans_instances = Sans.objects.filter(ConcertId=updated_concert)
                
                # Create Rows for each new Sans
                for sans in new_sans_instances:
                    rows_to_create = [
                        Rows(ConcertId=updated_concert, SansId=sans, RowNumber=j+1)
                        for j in range(current_number_of_rows)
                    ]
                    Rows.objects.bulk_create(rows_to_create)
                
            # Return the updated concert data
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Concert.DoesNotExist:
            return Response({"error": "Concert not found"}, status=status.HTTP_404_NOT_FOUND)


    def delete(self,request,id):
        concerts_obj = Concert.objects.get(ConcertId=id)
        concerts_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

   

#if seat status changed change its icon to other color it means change its icon
class ConcertDetail(APIView):
  
    def get(self,request,id,sansid):
        concerts = Concert.objects.all()
        seats = Seat.objects.all()
        sans = Sans.objects.filter(SansId=sansid)
        

        concert_serializer = ConcertSerializer(concerts, many=True)
        seat_serializer = SeatSerializer(seats, many=True)
        sans_serializer = SansSerializer(sans, many=True)
        
        return Response({
        'concerts': concert_serializer.data,
        'sans' : sans_serializer.data,
        'seats': seat_serializer.data
        
    }, status=status.HTTP_200_OK)

class RowsAdminView(APIView):
    def get(self, request, id=None):
        if id is not None:
        
            rows = Rows.objects.get(ConcertId=id)
            serializer = GetRowSerializer(rows)
            return Response(serializer.data)
        else:
            # List all concerts
            all_rows = Rows.objects.all()
            serializer = GetRowSerializer(all_rows, many=True)
            return Response(serializer.data)


    
class SeatsAdminView(APIView):
    # permission_classes = (IsAuthenticated,)
    
    def post(self, request, id, Rowid):
        data = request.data
        data['ConcertId'] = id
        data['Rowid'] = Rowid

        seatnumber = data['NumberofSeat']
        seatprice = data['RowPrice']  # Assuming SeatPrice is provided in the request
        rowarea = data['RowArea']  # Retrieve RowArea from the posted data

        serializer = CreateSeatsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        # Save the serialized data
        seats = serializer.save()

        # Update the NumberofSeat, RowPrice, and RowArea fields in the Rows model
        try:
            row = Rows.objects.get(ConcertId=id, Rowid=Rowid)
            row.NumberofSeat = seatnumber
            row.RowPrice = seatprice  # Set RowPrice equal to SeatPrice
            row.RowArea = rowarea  # Set RowArea to the posted value
            row.save()
        except Rows.DoesNotExist:
            return Response({"error": "Row not found"}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve existing seat numbers
        existing_seat_numbers = set(
            Seat.objects.filter(ConcertId=id, Rowid=Rowid).values_list('SeatNumber', flat=True)
        )

        # Create the seats if they do not already exist
        seats_to_create = [
            Seat(ConcertId=seats.ConcertId, Rowid=seats.Rowid, SeatNumber=i + 1, SeatPrice=seatprice)
            for i in range(seatnumber)
            if (i + 1) not in existing_seat_numbers
        ]

        # Perform bulk creation after collecting all seats to be created
        if seats_to_create:
            Seat.objects.bulk_create(seats_to_create)
            
        else:
            ## IF NULL NEEDED DELETE THIS 
            
            return Response({"error": "All seats already exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        Seat.objects.filter(ConcertId=id, Rowid=Rowid, SeatNumber__isnull=True,SeatStatus='Empty').delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, id, Rowid):
        # Retrieve seats for the given concert and row
        seats = Seat.objects.filter(ConcertId=id, Rowid=Rowid)
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)

    def put(self, request, id, Rowid, SeatId):
        data = request.data
        serializer = SeatSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        update = serializer.save()

        try:
            row = Rows.objects.get(ConcertId=id, Rowid=Rowid)
            number_of_seat = row.NumberofSeat
        except Rows.DoesNotExist:
            return Response({"error": "Row not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            seat = Seat.objects.get(ConcertId=id, Rowid=Rowid, SeatId=SeatId)
            seat.SeatStatus = update.SeatStatus

            if seat.SeatStatus == 'space':
                seat.SeatNumber = None
            else:
                for i in range(number_of_seat):
                    seat.SeatNumber = i + 1

            seat.save()
        except Seat.DoesNotExist:
            return Response({"error": "Seat not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)

class SelectSeat(APIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer




class UpdateSeatView(generics.UpdateAPIView):
    queryset = Seat.objects.all()
    serializer_class = UpdateSeatSerializer
    lookup_field = 'SeatId'
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data

        # Perform the update
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Check if the seat status is 'space' and SeatNumber is None
        if instance.SeatStatus == 'space' or instance.SeatNumber is None:
            instance.SeatStatus = 'space'
            instance.SeatNumber = None
            self.rename_seat_numbers(instance.ConcertId, instance.Rowid)

        return Response(serializer.data)

    def rename_seat_numbers(self, concert_id, row_id):
        seats = Seat.objects.filter(ConcertId=concert_id, Rowid=row_id).order_by('SeatId')
        seat_number = 1
        for seat in seats:
            if seat.SeatStatus != 'space':  # Only update seats that are not 'space'
                seat.SeatNumber = seat_number
                seat_number += 1
            else:
                seat.SeatNumber = None  # Ensure 'space' seats have SeatNumber as None
            seat.save()




class SansAdminView(APIView):

    def post(self,request,id):
        serializer = CreateSansSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        SansNumber = serializer.validated_data.get('SansNumber')
        ConcertId = serializer.validated_data.get('ConcertId')
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

    def get(self, request,id):
        if id is not None :
            try:
                concert = Concert.objects.get(ConcertId=id)
                all_sans = Sans.objects.filter(ConcertId=id)
                serializer = ConcertSerializer(concert)
                sans_serializer = SansSerializer(all_sans, many=True)
                return Response({
                    'concerts': serializer.data,
                    'sans': sans_serializer.data
                }, status=status.HTTP_200_OK)
            except Concert.DoesNotExist:
                return Response({'error': 'Concert not found'}, status=status.HTTP_404_NOT_FOUND)
            except Sans.DoesNotExist:
                return Response({'error': 'Sans not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # List all Sanes
            all_concerts = Concert.objects.all()
            
            serializer = ConcertSerializer(all_concerts, many=True)
            



    def put(self, request, id):
        # Retrieve the seat object to update
        Sans_obj = Sans.objects.get(ConcertId=id)
     #   Sans = Sans.objects.filter(SansId=sansid)  # Use filter instead of get




        # Update the seat object with the request data
        serializer = CreateSansSerializer(instance=Sans_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    
class SansUpdateView(UpdateAPIView):
    queryset = Sans.objects.all()
    serializer_class = UpdateSansSerializer
    lookup_field = 'SansId'
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data

       # Perform the update
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)



        

    

    