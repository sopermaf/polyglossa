'''
Tests for Payments/models
'''
# pylint: disable=missing-function-docstring
from .base_test import TestPayments
from ..models import Order


class TestOrders(TestPayments):
    '''Tests for models.Orders'''
    def test_success_status(self):
        self.order.success()

        self.assertEqual(
            self.order.payment_status, Order.PaymentStatus.COMPLETE
        )

    def test_success_complete_action(self):
        self.assertFalse(self.student_in_seminar(), 'Student absent')

        self.order.success()
        self.assertTrue(self.student_in_seminar(), 'Student added')

    def test_failure_status(self):
        self.order.failure()

        self.assertEqual(
            self.order.payment_status, Order.PaymentStatus.FAILED
        )

    def test_failure_student_not_added(self):
        self.assertFalse(self.student_in_seminar(), 'Student absent')
        self.order.failure()

        self.assertFalse(self.student_in_seminar(), 'Student absent')
