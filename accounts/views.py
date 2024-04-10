from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import Customer
from .serializers import CreateCustomerSerializer,CustomerSerializer
from rest_framework.generics import CreateAPIView

class CustomerLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        cu_phonenumber = request.data.get('cu_phonenumber')
        password = request.data.get('password')

        # Authenticate the customer
        user = authenticate(cu_phonenumber=cu_phonenumber, password=password)

        if user is not None:
            # Authentication successful
            return Response({'message': 'Login successful', 'customer_id': user.cu_id}, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
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