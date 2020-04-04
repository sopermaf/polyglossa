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
        self.assertFalse(
            self.slot.students.filter(pk=self.student.pk),
            'Student not in seminar'
        )

        self.order.success()

        self.assertTrue(
            self.slot.students.filter(pk=self.student.pk),
            'Student now added to seminar'
        )

    def test_failure_status(self):
        self.order.failure()

        self.assertEqual(
            self.order.payment_status, Order.PaymentStatus.FAILED
        )

    def test_failure_student_not_added(self):
        self.order.failure()

        self.assertFalse(
            self.slot.students.filter(pk=self.student.pk),
            'Student not in seminar'
        )
