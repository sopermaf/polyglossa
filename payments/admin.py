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
        'reference',
        'modified',
        'created',
    )
    date_hierarchy = 'modified'
    ordering = ['-modified', '-created', '-payment_received']
    list_filter = ('payment_status', 'modified', 'payment_received', 'created')
    search_fields = ('order_details', 'reference')
    readonly_fields = (
        'reference',
        'customer',
        'created',
        'modified',
        'payment_received',
        'processor',
        'order_details',
    )
