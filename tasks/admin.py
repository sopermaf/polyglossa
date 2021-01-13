# pylint: disable=missing-class-docstring,missing-module-docstring
from django.contrib import admin

from .models import EmailTask


@admin.register(EmailTask)
class EmailTaskAdmin(admin.ModelAdmin):
    list_display = ('subject', 'to_email', 'sent', 'created', 'modified')
    ordering = ('-modified', '-created')
    search_fields = ('subject', 'to_email')
    list_filter = ('sent', 'subject')
    readonly_fields = ('created', 'modified')
