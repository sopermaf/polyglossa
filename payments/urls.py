# pylint: disable=missing-module-docstring, invalid-name
from django.urls import path

from . import views

# Create your views here.
urlpatterns = [
    path('cancel/', views.cancel_awaiting_order, name='cancel-awaiting'),
    path('order/', views.order_page, name='order-page'),
]
