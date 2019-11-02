from django.shortcuts import render
from django.urls import path
from django.views.generic import TemplateView
from class_bookings import views

# Create your views here.
urlpatterns = [
    path("",
        TemplateView.as_view(template_name="bookClass.html"),
        name="index",
    ),
    path('create/', views.make_booking, name='create-booking'),
]