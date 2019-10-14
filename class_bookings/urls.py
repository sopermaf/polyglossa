from django.shortcuts import render
from django.urls import path
from django.views.generic import TemplateView

# Create your views here.
urlpatterns = [
    path("",
        TemplateView.as_view(template_name="bookClass.html"),
        name="booking",
    ),
]