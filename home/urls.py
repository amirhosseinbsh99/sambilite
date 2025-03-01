from django.urls import path
from home.views import ConcertAdminView,ListConcertView,SansAdminView,ConcertSearchView,SliderAdminView,ConcertDetail,SeatsAdminView,RowsAdminView,SansUpdateView,UpdateSeatView,RowsAdminView
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'home'

urlpatterns = [
        path('co-admin/Sliders/', SliderAdminView.as_view(), name='SliderAdminView'),
        path('co-admin/Sliders/<int:Sliderid>/', SliderAdminView.as_view(), name='UpdateSliderAdminView'),
        path('co-admin/Concerts/', ConcertAdminView.as_view(), name='ConcertAdminView'),
        path('co-admin/Concerts/Create/', ConcertAdminView.as_view(), name='CreateListConcertView'),
        path('co-admin/Concerts/<int:id>/', ConcertAdminView.as_view(), name='UpdateConcert'),
        path('co-admin/Concerts/<int:id>/Sans/', SansAdminView.as_view(), name='SansAdminView'),
        path('co-admin/Concerts/<int:id>/Sans/<int:SansId>/', SansUpdateView.as_view(), name='SansUpdateView'),
        path('co-admin/Concerts/<int:id>/Row/', RowsAdminView.as_view(), name='RowsAdminView'),
        path('co-admin/Concerts/<int:id>/Row/<int:Rowid>/Seats/Create/', SeatsAdminView.as_view(), name='CreateSeatsAdminView'),
        path('co-admin/Concerts/<int:id>/Row/<int:Rowid>/Seats/<int:SeatId>/', UpdateSeatView.as_view(), name='UpdateSeatsAdminView'),
        #################################### non-admins ##########################################################
        path('', ListConcertView.as_view(), name='ListConcertView'),
        path("Search/", ConcertSearchView.as_view()  , name = "ConcertSearchView"),
        path('Concerts/<int:id>/', ConcertDetail.as_view(), name='ConcertDetail'),
        path('Concerts/<int:id>/Sans/<int:sanid>/', ConcertDetail.as_view(), name='ConcertDetail'),
        path('about-us/',TemplateView.as_view(template_name='about-us'),name='about-us'),
        path('contact-us/',TemplateView.as_view(template_name='contact-us'),name='contact-us'),

        ###########################################################################################################
        

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)