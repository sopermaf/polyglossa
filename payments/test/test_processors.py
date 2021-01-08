'''
Tests for Payments/processors
'''
# pylint: disable=missing-function-docstring
import json
from tasks.models import EmailTask

from .base_test import TestPayments
from .. import processors


class TestProcessors(TestPayments):
    '''Tests for SeminarProcessor'''
    def setUp(self):
        super().setUp()
        self.serial_order = json.dumps(self.order_details)

    # Tests

    def test_seminar_complete(self):
        processor = processors.SemSlotProcessor(self.serial_order)

        self.assertFalse(self.student_in_seminar(), "Student absent")

        processor.complete()
        self.assertTrue(self.student_in_seminar(), "Student added")

    def test_email_task_created(self):
        # setup
        processor = processors.SemSlotProcessor(self.serial_order)
        processor.complete()

        # ensure emails is created
        email = EmailTask.objects.first()
        self.assertTrue(email, 'ensure email created')
        self.assertEqual(email.to_email, self.student.email)
