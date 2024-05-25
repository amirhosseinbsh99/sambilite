from rest_framework.response import Response
from .models import Concert,Seat,Sans,Rows,Payment,Ticket
from accounts.models import Customer
from rest_framework import generics
from .serializers import ConcertSerializer,CreateConcertSerializer,SeatSerializer,UpdateSeatSerializer,CreateSansSerializer,CreateSeatsSerializer,SansSerializer,GetRowSerializer,UpdateSansSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,UpdateAPIView
from django.utils import timezone
from datetime import timedelta,datetime
from rest_framework import filters 
from django.db import transaction
from rest_framework import generics
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
import requests
import json
from rest_framework.permissions import IsAuthenticated
from accounts.views import IsAdminUser


class ListConcertView(ListAPIView):

    def get(self, request):
        ip_response = requests.get('https://api.ipify.org/?format=json')
        ip_data = ip_response.json()
        myip = ip_data.get('ip')
        location_response = requests.get(f'http://ip-api.com/json/{myip}')
        location_data = location_response.json()
        city = location_data.get('city')
        concerts = Concert.objects.filter(ConcertLocation=city)
        if not concerts.exists():
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


     ##* for admin *##
class ConcertAdminView(APIView):
    permission_classes = [IsAdminUser]


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
                return Response({'error': 'کنسرت یافت نشد'}, status=status.HTTP_404_NOT_FOUND)
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
                existing_rows.delete()
                

                
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
                
                # Create new Sans 
                for i in range(new_number_of_Sans):
                    new_sans = Sans(ConcertId=updated_concert, SansNumber=i+1)
                    new_sans.save()
                
                # get the newly created Sans with primary keys
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
            return Response({"error": "کنسرت یافت نشد"}, status=status.HTTP_404_NOT_FOUND)


    def delete(self,request,id):
        try:
            concerts_obj = Concert.objects.get(ConcertId=id)
            concerts_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Concert.DoesNotExist:
            return Response({"error": "کنسرت یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
    

   

#if seat status changed change its icon to other color it means change its icon#
class ConcertDetail(APIView):

    def get(self,request,id):
        concerts = Concert.objects.filter(ConcertId=id)
        seats = Seat.objects.filter(ConcertId=id)
        sans = Sans.objects.filter(ConcertId=id)
        rows = Rows.objects.filter(ConcertId=id)

        concert_serializer = ConcertSerializer(concerts, many=True)
        seat_serializer = SeatSerializer(seats, many=True)
        sans_serializer = SansSerializer(sans, many=True)
        rows_serializer = GetRowSerializer(rows, many=True)
        return Response({
        'concerts': concert_serializer.data,
        'sans' : sans_serializer.data,
        'rows' : rows_serializer.data,
        'seats': seat_serializer.data

    }, status=status.HTTP_200_OK)

    def post(self, request, id):
        seat_id = request.data.get('seat_id')
        CustomerName = request.data.get('CustomerName')
        CustomerPhoneNumber = request.data.get('CustomerPhoneNumber')
        seat = get_object_or_404(Seat, pk=seat_id, ConcertId=id)
        
        if seat.SeatStatus not in ['Empty', 'Empty']:
            return Response({"error": "Seat is not available."}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            seat.SeatStatus = 'Reserving'
            seat.save()

            # Create temporary user for this transaction
            temp_user = Customer.objects.create(
                username=f"{CustomerName}_{CustomerPhoneNumber}",
                CustomerName=CustomerName,
                CustomerLocation='Temporary',
                is_admin=False
            )
            temp_user.set_unusable_password()
            temp_user.save()

            # Process payment (assuming a mock payment processing here)
            payment_status = 'Pending'
            payment = Payment.objects.create(
                TicketId=None,  # To be set later
                SeatId=seat,
                PaymentStatus=payment_status,
                CustomerId=temp_user
            )

            # Simulate payment process
            if self.process_payment(payment):  # Assuming this method handles the payment processing
                payment.PaymentStatus = 'Completed'
                payment.save()

                # Create ticket
                ticket = Ticket.objects.create(
                    Ticket_Serial='some_serial',  # Generate a unique serial here
                    SansId=seat.SansId,
                    SeatId=seat,
                    ConcertId=seat.ConcertId
                )
                payment.TicketId = ticket
                payment.save()

                seat.SeatStatus = 'Reserved'
                seat.save()
                return Response({"message": "Payment successful and ticket created."}, status=status.HTTP_201_CREATED)
            else:
                payment.PaymentStatus = 'Failed'
                payment.save()

                # Revert seat status
                seat.SeatStatus = 'Empty'
                seat.save()

                # Delete temporary user
                temp_user.delete()

                return Response({"error": "Payment failed."}, status=status.HTTP_400_BAD_REQUEST)




def process_payment(self, payment):
        # Implement actual payment processing logic here
        # Return True if payment is successful, otherwise False
        return True

class RowsAdminView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, id=None):
        try:
            if id is not None:
            
                rows = Rows.objects.get(ConcertId=id)
                serializer = GetRowSerializer(rows)
                return Response(serializer.data)
            else:
                all_rows = Rows.objects.all()
                serializer = GetRowSerializer(all_rows, many=True)
                return Response(serializer.data)
        except Concert.DoesNotExist:
                return Response({"error": "کنسرت یافت نشد"}, status=status.HTTP_404_NOT_FOUND) 


    
class SeatsAdminView(APIView):
    
    permission_classes = [IsAdminUser]
    def post(self, request, id, Rowid):
        data = request.data
        data['ConcertId'] = id
        data['Rowid'] = Rowid

        seatnumber = data['NumberofSeat']
        seatprice = data['RowPrice']  # Assuming SeatPrice is provided in the request
        rowarea = data['RowArea']  # Retrieve RowArea from the posted data

        serializer = CreateSeatsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        
        seats = serializer.save()

        # Update the NumberofSeat, RowPrice, and RowArea fields in the Rows model
        try:
            row = Rows.objects.get(ConcertId=id, Rowid=Rowid)
            row.NumberofSeat = seatnumber
            row.RowPrice = seatprice  
            row.RowArea = rowarea  
            row.save()
        except Rows.DoesNotExist:
            return Response({"error": " ردیف یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

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

        
        if seats_to_create:
            Seat.objects.bulk_create(seats_to_create)
            
        else:
           
            Seat.objects.filter(ConcertId=id, Rowid=Rowid, SeatNumber__isnull=True,SeatStatus='Empty').delete()
            return Response({"error": "صندلی تکراری است"}, status=status.HTTP_400_BAD_REQUEST)
        
        Seat.objects.filter(ConcertId=id, Rowid=Rowid, SeatNumber__isnull=True,SeatStatus='Empty').delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, id, Rowid):
        try:
            # Retrieve seats for the given concert and row
            seats = Seat.objects.filter(ConcertId=id, Rowid=Rowid)
            serializer = SeatSerializer(seats, many=True)
            return Response(serializer.data)
        except Rows.DoesNotExist:
            return Response({"error": "  ردیف یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id, Rowid, SeatId):
        data = request.data
        serializer = SeatSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        update = serializer.save()
        
        try:
            concert = Concert.objects.get(ConcertId=id) 
        except Concert.DoesNotExist:
            return Response({"error": "کنسرت پیدا نشد"}, status=status.HTTP_404_NOT_FOUND)

        try:
            row = Rows.objects.get(ConcertId=id, Rowid=Rowid)
            number_of_seat = row.NumberofSeat
        except Rows.DoesNotExist:
            return Response({"error": "  ردیف یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

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
            return Response({"error": "صندلی پیدا نشد"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)
    


class UpdateSeatView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Seat.objects.all()
    serializer_class = UpdateSeatSerializer
    lookup_field = 'SeatId'

    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        try:
            obj = queryset.get(**filter_kwargs)
        except Seat.DoesNotExist:
            raise NotFound({"error": "صندلی پیدا نشد"})  # 404 error if seat not found
        return obj
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data

        # Perform the update
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

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
                seat.SeatNumber = None  #And ensure that 'space' seats have SeatNumber as None
            seat.save()


class SansAdminView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, id):
        # Check if the concert exists
        try:
            concert = Concert.objects.get(id=id)
        except Concert.DoesNotExist:
            return Response({"error": "کنسرت پیدا نشد"}, status=status.HTTP_404_NOT_FOUND)

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
        elif Sans.objects.filter(SansTime=SansTime, ConcertId=ConcertId).exists():
            return Response({"message": "تکراری بودن زمان سانس"}, status=status.HTTP_400_BAD_REQUEST)
        elif Sans.objects.filter(SansNumber=SansNumber, ConcertId=ConcertId).exists():
            return Response({"message": f"سانس {SansNumber} وجود دارد"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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
                return Response({'error': 'کنسرت یافت نشد'}, status=status.HTTP_404_NOT_FOUND)
            except Sans.DoesNotExist:
                return Response({'error': 'سانس پیدا نشد'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # List all Sanes
            all_concerts = Concert.objects.all()
            
            serializer = ConcertSerializer(all_concerts, many=True)

class SansUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Sans.objects.all()
    serializer_class = UpdateSansSerializer
    lookup_field = 'SansId'

    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        try:
            obj = queryset.get(**filter_kwargs)
        except Sans.DoesNotExist:
            raise NotFound({"error": "سانس پیدا نشد"}) 
        return obj

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)