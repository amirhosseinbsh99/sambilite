from django.contrib import admin
from .models import Customer,Concert,Seat,Sans
from blog.models import Blog



class CustomerAdmin(admin.ModelAdmin):
    list_display = ("cu_name","username","cu_location")

class ConcertAdmin(admin.ModelAdmin):
    list_display = ("co_name","co_type","a_name")




class BlogAdmin(admin.ModelAdmin):

    list_display = ("b_name", "b_text", "b_type")

class SeatAdmin(admin.ModelAdmin):
    list_display = ('se_id','co_id','se_row', 'se_area','se_status')

class SansAdmin(admin.ModelAdmin):

    list_display = ("co_id","sa_number", "sa_time")

admin.site.register(Concert,ConcertAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(Blog,BlogAdmin)
admin.site.register(Seat,SeatAdmin)
admin.site.register(Sans,SansAdmin)