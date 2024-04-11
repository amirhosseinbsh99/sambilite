from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import Customer
from .serializers import CreateCustomerSerializer,CustomerSerializer,CustomerRegiserSerializer,CustomerLoginSerializer
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView


class CustomerLoginAPIView(APIView):
    def post(self, request):
        cu_phonenumber = request.data.get('cu_phonenumber')
        cu_password = request.data.get('cu_password')

        # Retrieve the user based on the phone number
        user = Customer.objects.filter(cu_phonenumber=cu_phonenumber).first()

        # If user exists, verify the password
        if user is not None and user.check_password(cu_password):
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
    queryset = Customer.objects.all()
    serializer_class = CreateCustomerSerializer


class CustomerRegister(APIView):
    def post(self, request):
        serializer = CustomerRegiserSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()

            data['response'] = 'اکانت شما با موفقیت ایجاد شد'
            data['name'] = account.cu_name
            data['email'] = account.cu_email

            token, _ = Token.objects.get_or_create(user=account)
            data['token'] = token.key
        else:
            data = serializer.errors

        return Response(data)

