# pylint: disable=missing-module-docstring, invalid-name
from django.urls import path

from . import views
from . import const

# Create your views here.
urlpatterns = [
    path('signup/seminar', views.post_seminar_student, name=const.SEMINAR_POST_NAME),
    path('get/seminar_slots/<int:seminar_id>', views.get_future_seminar_slots, name='sem-slots'),
    path('get/activities/<str:activity_type>', views.get_activities, name='get-activities')
]
