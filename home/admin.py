from django.contrib import admin
from .models import Customer, Concert, Seat, Sans, Rows, Slider, Order, OrderItem
from blog.models import Blog


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("fullname", "username", "phone_number")


class ConcertAdmin(admin.ModelAdmin):
    list_display = ("concert_name", "concert_type", "artist_name", "number_of_rows", "concert_status", "concert_date", "concert_location")


class SansAdmin(admin.ModelAdmin):
    list_display = ("concert", "sans_number", "sans_status", "sans_time", "sans_date")


class RowsAdmin(admin.ModelAdmin):
    list_display = ("concert", "row_number", "row_price", "row_area", "number_of_seat", "sans")


class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'row', 'seat_price', 'concert', 'seat_status')


class SliderAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "image", "url")


class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "seat", "payment_status", "created_at", "ref_id", "authority")


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "seat", "concert")


class BlogAdmin(admin.ModelAdmin):
    list_display = ("BlogTitle", "BlogDescription", "BlogType")


admin.site.register(Concert, ConcertAdmin)
admin.site.register(Sans, SansAdmin)
admin.site.register(Rows, RowsAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Customer, CustomerAdmin)
