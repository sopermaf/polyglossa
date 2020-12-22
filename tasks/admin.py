# pylint: disable=missing-class-docstring,missing-module-docstring
from django.contrib import admin

from .models import EmailTask


@admin.register(EmailTask)
class EmailTaskAdmin(admin.ModelAdmin):
    list_display = ('sent', 'subject', 'to_email', 'created', 'modified')
    ordering = ('modified', 'created')
    search_fields = ('subject', 'to_email')
    list_filter = ('sent', 'subject')
