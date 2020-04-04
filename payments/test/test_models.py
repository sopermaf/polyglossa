# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
import json

from django.test import TestCase

from class_bookings.test import util
from class_bookings import models as cb_models
from class_bookings import const

from ..models import Order


class TestOrders(TestCase):
    def setUp(self):
        self.student = cb_models.Student.objects.create(
            name='bob', email='bob@test.com'
        )

        activity = util.create_activity(
            activity_type=cb_models.Activity.SEMINAR,
            bookable=True,
        )
        slots = util.create_seminar_slots(activity)
        self.slot = slots['future']

        self.order = Order.objects.create(
            customer=self.student,
            payment_status=Order.PaymentStatus.AWAITING,
            processor=Order.ProcessorEnums.SEMINAR,
            order_details=json.dumps({
                const.KEY_CHOICE: self.slot.id,
                const.KEY_NAME: self.student.name,
                const.KEY_EMAIL: self.student.email,
            }),
        )

    # Tests

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
