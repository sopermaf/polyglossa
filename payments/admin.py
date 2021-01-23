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
    search_fields = ('reference', 'customer__name', 'customer__email')
    readonly_fields = (
        'reference',
        'customer',
        'purchased_detail',
        'created',
        'modified',
        'payment_received',
        'processor',
        'processor_data',
    )
