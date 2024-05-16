from django.contrib import admin
from .models import Customer,Concert,Seat,Sans,Rows
from blog.models import Blog



class CustomerAdmin(admin.ModelAdmin):
    list_display = ("CustomerName","username","CustomerLocation")

class ConcertAdmin(admin.ModelAdmin):
    list_display = ("ConcertName","ConcertType","ArtistName","NumberofRows")


class RowsAdmin(admin.ModelAdmin):
    list_display = ("ConcertId", "Rowid", "RowNumber","RowPrice")

class BlogAdmin(admin.ModelAdmin):

    list_display = ("BlogTitle", "BlogDescription", "BlogType")

class SeatAdmin(admin.ModelAdmin):
    list_display = ('SeatId','ConcertId','SeatRow', 'SeatArea','SeatStatus')

class SansAdmin(admin.ModelAdmin):

    list_display = ("ConcertId","SansNumber", "SansTime")



admin.site.register(Concert,ConcertAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(Blog,BlogAdmin)
admin.site.register(Seat,SeatAdmin)
admin.site.register(Sans,SansAdmin)
admin.site.register(Rows,RowsAdmin)
