from django.contrib import admin
from .models import Customer,Concert

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("cu_name","cu_phonenumber")

class ConcertAdmin(admin.ModelAdmin):
    list_display = ("co_name","co_type")


admin.site.register(Concert,ConcertAdmin)
admin.site.register(Customer,CustomerAdmin)

