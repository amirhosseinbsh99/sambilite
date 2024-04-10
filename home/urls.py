from django.urls import path
from home.views import ConcertView,ListConcertView,CreateListConcertView,ConcertSearchView


app_name = 'home'

urlpatterns = [
        path('Concerts/', ConcertView.as_view(), name='ConcertView'),
        path('Concerts/<int:id>/', ConcertView.as_view(), name='edit_ConcertView'),
        path('Concerts/create/', CreateListConcertView.as_view(), name='CreateListConcertView'),
        path('', ListConcertView.as_view(), name='ListConcertView'),

        path("Search/", ConcertSearchView.as_view()  , name = "ConcertSearchView"),
        



]
