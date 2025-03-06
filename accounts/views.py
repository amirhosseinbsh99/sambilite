from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import Customer
from .serializers import CreateCustomerSerializer,CustomerSerializer,CustomerLoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import BasePermission


# CHANGE TO KHARID BILITE
class CustomerLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Retrieve the user based on the phone number
        user = Customer.objects.filter(username=username).first()

        # If user exists, verify the password
        if user is not None and user.check_password(password):
            # Authentication successful
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class CustomerView(APIView):
    def post(self,request):
        serializer = CreateCustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def get(self, request, id=None):  
        if id is not None:
        
            customer = Customer.objects.get(CustomerId=id)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        else:
            # List all concerts
            all_Customer = Customer.objects.all()
            serializer = CustomerSerializer(all_Customer, many=True)
            return Response(serializer.data)



    def put(self,request,id): 
           customers_obj = Customer.objects.get(CustomerId=id)
           serializer = CreateCustomerSerializer(instance=customers_obj,data=request.data)
           serializer.is_valid(raise_exception=True)
           serializer.save()
           return Response(serializer.data)



    def delete(self,request,id):
        customers_obj = Customer.objects.get(CustomerId=id)
        customers_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateCustomerView(CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CreateCustomerSerializer

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and is an admin
        return bool(request.user and request.user.is_authenticated and request.user.is_admin)