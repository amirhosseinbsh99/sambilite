from django.urls import path
from accounts.views import CustomerLoginAPIView ,CustomerView,CreateCustomerView

app_name = 'account'

urlpatterns = [
    path('login/',CustomerLoginAPIView.as_view() ,name='CustomerLogin' ),
        
                            
    path('customer/', CustomerView.as_view(), name='CustomerView'),
    path('customer/<int:id>/', CustomerView.as_view(), name='EditCustomerView'),
    path('customer/Create/', CreateCustomerView.as_view(), name='CreateCustomerView')
]
