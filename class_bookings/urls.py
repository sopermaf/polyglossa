# pylint: disable=missing-module-docstring, invalid-name
from django.urls import path

from . import views

# Create your views here.
urlpatterns = [
    path('signup/seminar', views.seminar_signup, name='signup-seminar'),
    path('get/seminar_slots/<int:seminar_id>', views.get_future_seminar_slots, name='sem-slots'),
    path('get/seminars/upcoming/', views.get_upcoming_seminars, name='get-upcoming-seminars'),
    path('get/activities/<str:activity_type>', views.get_activities, name='get-activities'),
    path('seminar/video/<uuid:slot_id>', views.seminar_video_page, name='video-view'),
]
