from django.contrib import admin
from .models import Order
# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ Settings for orders in admin """
    list_display = (
        'date',
        'order_number',
        'full_name',
        'email',
        'phone_number',
    )
