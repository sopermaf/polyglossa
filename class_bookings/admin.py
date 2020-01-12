'''These are the tables which
can be modified by admins on polyglossa
contained in the class_booking app
'''
from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Student)
admin.site.register(models.Activity)
admin.site.register(models.SeminarSlot)
admin.site.register(models.IndividualSlot)
