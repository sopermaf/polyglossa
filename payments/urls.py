# pylint: disable=missing-module-docstring, invalid-name
from django.urls import path

from . import views

# Create your views here.
urlpatterns = [
    path('pay/', views.paypal_form, name='payment-form'),
    path('complete/', views.payment_complete, name='payment-complete'),
    path('cancelled/', views.payment_cancelled, name='payment-cancelled'),
]
