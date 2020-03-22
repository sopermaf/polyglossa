'''
Admin interface for payments in Polyglossa
'''
from django.contrib import admin
from . import models

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    '''Admin Interface for Order model'''
    list_display = (
        'payment_status',
        'customer',
        'processor',
        'modified',
        'created',
        'order_details',
    )
    ordering = ['payment_status', 'created', 'modified']

admin.site.register(models.Order, OrderAdmin)
