'''These are the tables which
can be modified by admins on polyglossa
contained in the class_booking app
'''
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


class IndividualSlotAdmin(admin.ModelAdmin):
    list_display = ('start_datetime', 'duration_in_mins', 'lesson', 'student')


admin.site.register(models.Activity, ActivityAdmin)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.SeminarSlot, SeminarSlotAdmin)
admin.site.register(models.IndividualSlot, IndividualSlotAdmin)
