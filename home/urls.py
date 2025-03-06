from django.urls import path
from home.views import ConcertAdminView,ListConcertView,SansAdminView,ConcertSearchView,SliderAdminView,ConcertDetail,SeatsAdminView,RowsAdminView,SansUpdateView,UpdateSeatView,RowsAdminView
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'home'

urlpatterns = [
        path('co-admin/sliders/', SliderAdminView.as_view(), name='SliderAdminView'),
        path('co-admin/sliders/<int:sliderid>/', SliderAdminView.as_view(), name='UpdateSliderAdminView'),
        path('co-admin/concerts/', ConcertAdminView.as_view(), name='ConcertAdminView'),
        path('co-admin/concerts/create/', ConcertAdminView.as_view(), name='CreateListConcertView'),
        path('co-admin/concerts/<int:id>/', ConcertAdminView.as_view(), name='UpdateConcert'),
        path('co-admin/concerts/<int:id>/sans/', SansAdminView.as_view(), name='SansAdminView'),
        path('co-admin/concerts/<int:id>/sans/<int:sansid>/', SansUpdateView.as_view(), name='SansUpdateView'),
        path('co-admin/concerts/<int:id>/row/', RowsAdminView.as_view(), name='RowsAdminView'),
        path('co-admin/concerts/<int:id>/row/<int:rowid>/seats/create/', SeatsAdminView.as_view(), name='CreateSeatsAdminView'),
        path('co-admin/concerts/<int:id>/row/<int:rowid>/seats/<int:seatid>/', UpdateSeatView.as_view(), name='UpdateSeatsAdminView'),
        #################################### non-admins ##########################################################
        path('', ListConcertView.as_view(), name='ListConcertView'),
        path("search/", ConcertSearchView.as_view()  , name = "ConcertSearchView"),
        path('concerts/<int:id>/', ConcertDetail.as_view(), name='ConcertDetail'),
        path('concerts/<int:id>/sans/<int:sanid>/', ConcertDetail.as_view(), name='ConcertDetail'),


        ###########################################################################################################
        

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)