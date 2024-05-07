from django.urls import path
from home.views import ConcertAdminView,ListConcertView,SansAdminView,CreateListConcertView,ConcertSearchView,ConcertDetail,SeatsAdminView
from django.views.generic import TemplateView


app_name = 'home'

urlpatterns = [
        path('co-admin/Concerts/', ConcertAdminView.as_view(), name='ConcertAdminView'),
        path('co-admin/Concerts/<int:id>/', ConcertAdminView.as_view(), name='EditConcertView'),
        path('co-admin/Concerts/create/', CreateListConcertView.as_view(), name='CreateListConcertView'),
        path('', ListConcertView.as_view(), name='ListConcertView'),
        path("Search/", ConcertSearchView.as_view()  , name = "ConcertSearchView"),
        path('Concerts/<int:id>/', ConcertDetail.as_view(), name='ConcertDetail'),
        path('co-admin/Seats/', SeatsAdminView.as_view(), name='SeatsAdminView'),
        path('co-admin/Seats/<int:id>/', SeatsAdminView.as_view(), name='EditSeatsAdminView'),
        path('co-admin/Seats/create/', SeatsAdminView.as_view(), name='CreateSeatsAdminView'),
        path('co-admin/Sans/create/', SansAdminView.as_view(), name='CreateSansAdminView'),
        path('co-admin/Sans/<int:id>/', SansAdminView.as_view(), name='EditSansAdminView'),
        path('co-admin/Sans/', SansAdminView.as_view(), name='SansAdminView'),
        path('about-us',TemplateView.as_view(template_name='about-us'),name='about-us'),
        path('contact-us',TemplateView.as_view(template_name='contact-us'),name='contact-us')
]


# co-admin/Concerts/
# co-admin/Concerts/<int:id>/
# co-admin/Concerts/create/'
# Search/
# Concerts/<int:id>/
# co-admin/Seats/
# co-admin/Seats/<int:id>/
# co-admin/Seats/create/
# co-admin/Sans/create/
# co-admin/Sans/<int:id>/
# co-admin/Sans/