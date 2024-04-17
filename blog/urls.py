from django.urls import path
from .views import BlogView,BlogCreateView,AddChoiceAPIView


app_name = 'blog'

urlpatterns = [
        path('', BlogView.as_view(), name='BlogView'),
        path('Create/', BlogCreateView.as_view(), name='BlogCreateView'),
        path('Create/add-choice', AddChoiceAPIView.as_view(), name='AddChoiceAPIView'),
        path('Create/', BlogCreateView.as_view(), name='BlogCreateView')





]