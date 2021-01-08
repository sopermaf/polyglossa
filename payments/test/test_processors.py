'''
Tests for Payments/processors
'''
# pylint: disable=missing-function-docstring
import json

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
