# pylint: disable=missing-module-docstring
from django.urls import path
from django.views.generic import TemplateView
from class_bookings import views
import class_bookings.util as class_bookings_utils

# Create your views here.
urlpatterns = [     # pylint: disable=invalid-name
    path(
        "",
        TemplateView.as_view(template_name="bookClass.html"),
        name="index",
    ),
    path(
        'create/', views.post_booking,
        name=class_bookings_utils.POST_LESSON_URL_NAME
    ),
]
