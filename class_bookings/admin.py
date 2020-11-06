'''
Admin interface for the class booking
app. Includes display changes for
models to sort them and give a better overview
'''
# pylint: disable=missing-class-docstring

from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from . import models


class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')


class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        'activity_type',
        'title',
        'price',
        'is_bookable',
        'is_highlighted',
        'order_shown'
    )
    fields = (
        'activity_type',
        'title',
        'description',
        ('price', 'is_bookable'),
        ('order_shown', 'is_highlighted'),
    )
    ordering = ['order_shown', 'activity_type', 'title']


class SeminarSlotAdmin(admin.ModelAdmin):
    def video_page_url(self):
        """Quick access to the video page"""
        return mark_safe("<a href='{0}'>View</a>".format(
            reverse('video-view', kwargs={'slot_id': self.external_id})
        ))

    list_display = (
        'start_datetime',
        'duration_in_mins',
        'seminar',
        video_page_url
    )
    ordering = ['start_datetime']


class IndividualSlotAdmin(admin.ModelAdmin):
    list_display = ('start_datetime', 'duration_in_mins', 'lesson', 'student')
    ordering = ['start_datetime']


admin.site.register(models.Activity, ActivityAdmin)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.SeminarSlot, SeminarSlotAdmin)
admin.site.register(models.IndividualSlot, IndividualSlotAdmin)
