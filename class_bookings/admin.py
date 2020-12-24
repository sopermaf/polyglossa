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


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    list_filter = ('name', 'email')
    search_fields = ('name', 'email')


@admin.register(models.Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'price',
        'is_bookable',
        'is_highlighted',
        'order_shown'
    )
    fields = (
        'activity_type',
        'price',
        ('is_bookable', 'is_highlighted'),
        'title',
        'description',
        'order_shown',
    )
    ordering = ['order_shown', 'activity_type', 'title']
    search_fields = ('title', 'description')
    list_filter = ('is_bookable', 'is_highlighted')


@admin.register(models.SeminarSlot)
class SeminarSlotAdmin(admin.ModelAdmin):
    def video_link(self):
        """Quick access to the video page"""
        return mark_safe("<a href='{0}'>{0}</a>".format(
            reverse('video-view', kwargs={'slot_id': self.external_id})
        ))

    def youtube_link(self):
        """Quick access to the video page"""
        link = "https://youtube.com/watch?v={}".format(self.video_id)
        return mark_safe("<a href='{0}'>{0}</a>".format(link))

    def reminder_sent(self):
        """Confirm some reminder with link has been sent"""
        return self.day_before_reminder_sent or self.hour_before_reminder_sent
    reminder_sent.boolean = True

    fields = (
        'seminar', 'video_id', 'start_datetime', 'duration_in_mins', 'students',
        'youtube_link', 'day_before_reminder_sent', 'hour_before_reminder_sent',
    )
    list_display = (
        'seminar',
        'start_datetime',
        video_link,
        youtube_link,
        reminder_sent,
    )
    list_filter = ('seminar', 'start_datetime')
    date_hierarchy = 'start_datetime'
    autocomplete_fields = ('seminar', 'students')
    ordering = ['start_datetime', 'seminar']
    readonly_fields = ('youtube_link', 'day_before_reminder_sent', 'hour_before_reminder_sent')
