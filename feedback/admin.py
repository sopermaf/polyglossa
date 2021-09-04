# pylint: missing-class-docstring, missing-module-docstring
from django.contrib import admin

from . import models


@admin.register(models.FeedbackType)
class FeedbackTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'feedback_type',
        'status',
        'reference',
        'modified',
        'created',
    )
    ordering = ('-modified', '-created')
    search_fields = ('reference', 'detail')
    list_filter = ('feedback_type', 'status')
    readonly_fields = ('created', 'modified')
