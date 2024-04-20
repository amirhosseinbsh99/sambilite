from django.urls import path
from home.views import ConcertAdminView,ListConcertView,CreateListConcertView,ConcertSearchView,ConcertDetailView


app_name = 'home'

urlpatterns = [
        path('co-admin/Concerts/', ConcertAdminView.as_view(), name='ConcertAdminView'),
        path('co-admin/Concerts/<int:id>/', ConcertAdminView.as_view(), name='ConcertAdminView'),
        path('co-admin/Concerts/create/', CreateListConcertView.as_view(), name='CreateListConcertView'),
        path('', ListConcertView.as_view(), name='ListConcertView'),
        path("Search/", ConcertSearchView.as_view()  , name = "ConcertSearchView"),
        path('Concerts/<int:id>/', ConcertDetailView.as_view(), name='ConcertDetailView')

        
]
