'''
Tests for Payments/models
'''
# pylint: disable=missing-function-docstring
from tasks.models import EmailTask
from .base_test import TestPayments
from ..models import Order


class TestOrders(TestPayments):
    '''Tests for models.Orders'''
    def test_success_status(self):
        self.assertFalse(self.order.payment_received)
        self.order.success()

        self.assertEqual(
            self.order.payment_status, Order.PaymentStatus.COMPLETED
        )
        self.assertTrue(self.order.payment_received)

        # order confirmed email and seminar details email
        self.assertEqual(EmailTask.objects.count(), 2, 'Email created')

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
