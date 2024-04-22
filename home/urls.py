from django.urls import path
from home.views import ConcertAdminView,ListConcertView,CreateListConcertView,ConcertSearchView,ConcertDetail,SeatsAdminView


app_name = 'home'

urlpatterns = [
        path('co-admin/Concerts/', ConcertAdminView.as_view(), name='ConcertAdminView'),
        path('co-admin/Concerts/<int:id>/', ConcertAdminView.as_view(), name='edit_ConcertView'),
        path('co-admin/Concerts/create/', CreateListConcertView.as_view(), name='CreateListConcertView'),
        path('', ListConcertView.as_view(), name='ListConcertView'),
        path("Search/", ConcertSearchView.as_view()  , name = "ConcertSearchView"),
        path("Search/", ConcertSearchView.as_view()  , name = "ConcertSearchView"),
        path('Concerts/<int:id>/', ConcertDetail.as_view(), name='ConcertDetail'),
        path('co-admin/Seats/', SeatsAdminView.as_view(), name='SeatsAdminView'),
        path('co-admin/Seats/<int:id>/', SeatsAdminView.as_view(), name='edit_SeatsAdminView'),
        path('co-admin/Seats/create/', SeatsAdminView.as_view(), name='CreateSeatsAdminView'),

        
]
