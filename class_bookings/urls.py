# pylint: disable=missing-module-docstring
from django.urls import path

from class_bookings import views
import class_bookings.util as class_bookings_utils

# Create your views here.
urlpatterns = [     # pylint: disable=invalid-name
    path(
        "",
        views.get_form,
        name="index",
    ),
    path(
        'create/',
        views.post_booking,
        name=class_bookings_utils.POST_LESSON_URL_NAME
    ),
]
