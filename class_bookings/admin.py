'''These are the tables which
can be modified by admins on polyglossa
contained in the class_booking app
'''
from django.contrib import admin
from .models import Student, LessonType, Booking

# Register your models here.
admin.site.register(Student)
admin.site.register(LessonType)
admin.site.register(Booking)
