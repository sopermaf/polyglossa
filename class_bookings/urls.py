# pylint: disable=missing-module-docstring, invalid-name
from django.urls import path

from . import views
from . import const

# Create your views here.
urlpatterns = [
    path(
        'signup/seminar',
        views.seminar_booking,
        name=const.SEMINAR_POST_NAME
    ),
]
