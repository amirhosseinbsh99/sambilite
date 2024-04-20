from django.contrib import admin
from .models import Customer,Concert
from blog.models import Blog



class CustomerAdmin(admin.ModelAdmin):
    list_display = ("cu_name","username","cu_location")

class ConcertAdmin(admin.ModelAdmin):
    list_display = ("co_name","co_type",'min_price', 'max_price','a_name')

    def min_price(self, obj):
        return obj.price_range[0]

    def max_price(self, obj):
        return obj.price_range[1]

    min_price.short_description = 'Min Price'
    max_price.short_description = 'Max Price'
    


class BlogAdmin(admin.ModelAdmin):

    list_display = ("b_name", "b_text", "b_type")

admin.site.register(Concert,ConcertAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(Blog,BlogAdmin)