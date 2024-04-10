from django.urls import path
from .views import CustomerLoginAPIView ,CustomerView,CreateCustomerView



urlpatterns = [
    path('login/',CustomerLoginAPIView.as_view() ,name='CustomerLogin' ),
   # path('registerrr/',CreateCustomerView.as_view(),name='CreateCustomerView'),
        
                             #after front given ###
    path('Customer/', CustomerView.as_view(), name='CustomerView'),
    path('Customer/<int:id>/', CustomerView.as_view(), name='EditCustomerView'),

]
