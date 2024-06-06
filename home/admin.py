from django.contrib import admin
from .models import Customer,Concert,Seat,Sans,Rows,Slider
from blog.models import Blog
from django_jalali.admin.widgets import AdminjDateWidget


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("CustomerName","username","CustomerPhoneNumber")

class ConcertAdmin(admin.ModelAdmin):
    list_display = ("ConcertName","ConcertType","ArtistName","NumberofRows")


class RowsAdmin(admin.ModelAdmin):
    list_display = ("ConcertId","SansId", "Rowid","RowNumber","RowPrice","RowArea")


class BlogAdmin(admin.ModelAdmin):

    list_display = ("BlogTitle", "BlogDescription", "BlogType")

class SeatAdmin(admin.ModelAdmin):
    list_display = ('SeatId','Rowid','SeatNumber','SeatPrice','ConcertId', 'SeatStatus')

class SansAdmin(admin.ModelAdmin):
    list_display = ("ConcertId","SansNumber", "SansTime")

class SliderAdmin(admin.ModelAdmin):
    list_display = ("ConcertId","title")

admin.site.register(Slider,SliderAdmin)
admin.site.register(Concert,ConcertAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(Blog,BlogAdmin)
admin.site.register(Seat,SeatAdmin)
admin.site.register(Sans,SansAdmin)
admin.site.register(Rows,RowsAdmin)
