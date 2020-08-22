# pylint: disable=missing-module-docstring, invalid-name
from django.urls import path

from . import views

# Create your views here.
urlpatterns = [
    path('get-all/', views.get_all_materials, name='get-all-materials'),
]
