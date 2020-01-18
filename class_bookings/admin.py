'''
Admin interface for the class booking
app. Includes display changes for
models to sort them and give a better overview
'''
# pylint: disable=missing-class-docstring

from django.contrib import admin
from . import models


class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_type', 'title', 'price', 'is_bookable')
    fields = (
        'activity_type',
        'title',
        ('price', 'is_bookable'),
        'description'
    )


class SeminarSlotAdmin(admin.ModelAdmin):
    list_display = ('start_datetime', 'duration_in_mins', 'seminar')
    ordering = ['start_datetime']


class IndividualSlotAdmin(admin.ModelAdmin):
    list_display = ('start_datetime', 'duration_in_mins', 'lesson', 'student')
    ordering = ['start_datetime']


admin.site.register(models.Activity, ActivityAdmin)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.SeminarSlot, SeminarSlotAdmin)
admin.site.register(models.IndividualSlot, IndividualSlotAdmin)
