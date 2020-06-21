'''
Tests for payments.views
'''
# pylint: disable=missing-function-docstring
from django.test import Client
from django.urls import reverse

from .base_test import TestPayments
from ..models import Order


class TestViews(TestPayments):
    '''Tests for payments.views'''
    # pylint: disable=no-self-use

    def setUp(self):
        super().setUp()
        self.client = Client()


    def test_cancel_order_success(self):
        # setup cookie from `payments.views.paypal_button`
        session = self.client.session
        session['order_id'] = self.order.id
        session.save()

        self.client.post(reverse('cancel-awaiting'))
        self.assertEqual(
            Order.objects.get(id=self.order.id).payment_status,
            Order.PaymentStatus.FAILED,
            "Order Status Updated"
        )

    def test_cancel_order_not_found(self):
        response = self.client.post(
            reverse('cancel-awaiting'),
        )
        self.assertEqual(response.status_code, 404, "Bad Request")
