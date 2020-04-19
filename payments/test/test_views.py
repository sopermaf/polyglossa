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
        response = self.client.post(
            reverse('cancel-awaiting'),
            data={
                'name': self.student.name,
                'email': self.student.email,
            }
        )

        self.assertEqual(response.status_code, 200, "Success code")
        self.assertEqual(
            Order.objects.get(id=1).payment_status,
            Order.PaymentStatus.FAILED,
            "Order Status Updated"
        )


    def test_cancel_order_not_found(self):
        response = self.client.post(
            reverse('cancel-awaiting'),
            data={'name': 'not real', 'email': 'not real'}
        )
        self.assertEqual(response.status_code, 404, "Bad Request")


    def test_cancel_order_missing_params(self):
        response = self.client.post(reverse('cancel-awaiting'))
        self.assertEqual(response.status_code, 400, "Missing parameters")
