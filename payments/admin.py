'''
Admin interface for payments in Polyglossa
'''
from django.contrib import admin
from . import models

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    '''Admin Interface for Order model'''
    list_display = (
        'payment_status',
        'customer',
        'amount',
        'modified',
        'created',
    )
    date_hierarchy = 'created'
    ordering = ['-modified', '-created']
    list_filter = ('payment_status', 'created', 'modified', 'customer', 'amount')
    search_fields = ('order_details', )
    readonly_fields = ('customer', 'created', 'modified', 'processor', 'order_details')
