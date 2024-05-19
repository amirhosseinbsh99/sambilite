from django.urls import path
from home.views import ConcertAdminView,ListConcertView,SansAdminView,ConcertSearchView,ConcertDetail,SeatsAdminView,RowsAdminView
from django.views.generic import TemplateView


app_name = 'home'

urlpatterns = [
        path('co-admin/Concerts/', ConcertAdminView.as_view(), name='ConcertAdminView'),
        path('co-admin/Concerts/<int:id>/', ConcertAdminView.as_view(), name='EditConcertView'),
        path('co-admin/Concerts/create/', ConcertAdminView.as_view(), name='CreateListConcertView'),
        path('co-admin/Concerts/<int:id>/generate-rows/', ConcertAdminView.as_view(), name='generate_rows'),
        path('', ListConcertView.as_view(), name='ListConcertView'),
        path("Search/", ConcertSearchView.as_view()  , name = "ConcertSearchView"),
        path('Concerts/<int:id>/', ConcertDetail.as_view(), name='ConcertDetail'),
        path('co-admin/Seats/<int:id>/', SeatsAdminView.as_view(), name='EditSeatsAdminView'),
        path('co-admin/Rows/', RowsAdminView.as_view(), name='RowsAdminView'),
        path('co-admin/Concerts/<int:id>/Row/<int:Rowid>/Seats/create', SeatsAdminView.as_view(), name='SeatsAdminView'),
        #path('co-admin/Concerts/<int:id>/Seats/<int:row_id>/generate-seats/<int:start>/<int:end>/', GenerateSeats.as_view(), name='GenerateSeats'),
        path('co-admin/Sans/create/', SansAdminView.as_view(), name='CreateSansAdminView'),
        path('co-admin/Sans/<int:id>/', SansAdminView.as_view(), name='EditSansAdminView'),
        path('co-admin/Sans/', SansAdminView.as_view(), name='SansAdminView'),
        path('about-us',TemplateView.as_view(template_name='about-us'),name='about-us'),
        path('contact-us',TemplateView.as_view(template_name='contact-us'),name='contact-us')
]
