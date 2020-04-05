# pylint: disable=missing-module-docstring, invalid-name
from django.urls import path

from . import views

# Create your views here.
urlpatterns = [
    path('pay/', views.paypal_form, name='payment-form'),
    path('button/', views.paypal_button, name='paypal-button'),
]
