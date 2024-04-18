from django.urls import path
from accounts.views import CustomerLoginAPIView ,CustomerView,CreateCustomerView

app_name = 'account'

urlpatterns = [
    path('login/',CustomerLoginAPIView.as_view() ,name='CustomerLogin' ),
   # path('register/',CustomerRegister.as_view(),name='CustomerRegister'),
        
                             #after front given ###
    path('Customer/', CustomerView.as_view(), name='CustomerView'),
    path('Customer/<int:id>/', CustomerView.as_view(), name='EditCustomerView'),
    path('Customer/Create', CreateCustomerView.as_view(), name='CreateCustomerView')
]
