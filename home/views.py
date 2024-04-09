from rest_framework.response import Response
from .models import Concert,Customer
from .serializers import ConcertSerializer,CreateConcertSerializer,CreateCustomerSerializer,CustomerSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework import viewsets
from django.utils import timezone
from datetime import timedelta,datetime
from rest_framework import filters  
from rest_framework.authtoken.models import Token

#for updating put
#from rest_framework.parsers import MultiPartParse

viewsets.ModelViewSet

#generic views
class ListConcertView(ListAPIView):
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
#class base
class ConcertView(APIView):
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



    def put(self,request,id): 
           concerts_obj = Concert.objects.get(co_id=id)
           serializer = CreateConcertSerializer(instance=concerts_obj,data=request.data)
           serializer.is_valid(raise_exception=True)
           serializer.save()
           return Response(serializer.data)



    def delete(self,request,id):
        concerts_obj = Concert.objects.get(co_id=id)
        concerts_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CustomerView(APIView):
    def post(self,request):
        serializer = CreateCustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def get(self, request, id=None):  
        if id is not None:
        
            customer = Customer.objects.get(cu_id=id)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        else:
            # List all concerts
            all_Customer = Customer.objects.all()
            serializer = CustomerSerializer(all_Customer, many=True)
            return Response(serializer.data)



    def put(self,request,id): 
           customers_obj = Customer.objects.get(cu_id=id)
           serializer = CreateCustomerSerializer(instance=customers_obj,data=request.data)
           serializer.is_valid(raise_exception=True)
           serializer.save()
           return Response(serializer.data)



    def delete(self,request,id):
        customers_obj = Customer.objects.get(cu_id=id)
        customers_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class CreateCustomerView(CreateAPIView):
    queryset = Concert.objects.all()
    serializer_class = CreateCustomerSerializer


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()

            # Assuming you have a user field in your Customer model
            # If not, adjust accordingly to create a user object
            user = customer.user  # Assuming user is the OneToOneField to the Django User model

            # Create a token for the user
            token = Token.objects.create(user=user)

            # Serialize the customer data
            json = serializer.data

            # Add the token to the response data
            json['token'] = token.key

            return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        

    

    