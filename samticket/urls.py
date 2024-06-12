
from django.contrib import admin
from django.urls import path,include
import zarrinpal

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('accounts/',include('accounts.urls')),
    path('blog/',include('blog.urls')),
    path('zarinpal/', include(zarinpal_urls)),

]
