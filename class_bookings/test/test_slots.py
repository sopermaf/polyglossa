# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, wildcard-import, unused-wildcard-import
from datetime import datetime, timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError

from payments.models import Order

from class_bookings.models import *

from . import util as t_util


# TODO: test slot range creation tests
# TODO: filter by state where available
# TODO: validation test for awaiting

class TestSlots(TestCase):
    def setUp(self):
        slot_dt = datetime.now() + timedelta(hours=2)
        self.slot = BaseSlot(start_datetime=slot_dt, duration_in_mins=60)
        self.slot.clean()
        self.slot.save()

    # Tests

    def test_start_at_end_of_slot(self):
        new_slot = BaseSlot(start_datetime=self.slot.end_datetime)
        new_slot.safe_save()

    def test_new_slot_inside_existing(self):
        start_dt = self.slot.start_datetime + timedelta(minutes=1)
        new_slot = BaseSlot(start_datetime=start_dt, duration_in_mins=5)

        # ensure test setup correctly
        self.assertLess(
            self.slot.start_datetime, new_slot.start_datetime, 'new start after existing start'
        )
        self.assertGreater(
            self.slot.end_datetime, new_slot.end_datetime, 'new end before existing end'
        )

        with self.assertRaises(ValidationError):
            new_slot.safe_save()

    def test_new_slot_contains_existing(self):
        start_dt = self.slot.start_datetime - timedelta(minutes=10)
        new_slot = BaseSlot(start_datetime=start_dt, duration_in_mins=120)

        # ensure test setup correctly
        self.assertLess(
            new_slot.start_datetime, self.slot.start_datetime, 'new start before existing start'
        )
        self.assertGreater(
            new_slot.end_datetime, self.slot.end_datetime, 'new end after existing existing end'
        )

        with self.assertRaises(ValidationError):
            new_slot.safe_save()

    def test_new_slot_start_overlaps(self):
        start_dt = self.slot.start_datetime + timedelta(minutes=10)
        new_slot = BaseSlot(start_datetime=start_dt, duration_in_mins=70)

        self.assertGreater(
            new_slot.start_datetime, self.slot.start_datetime, 'new start after existing start'
        )
        self.assertLess(
            new_slot.start_datetime, self.slot.end_datetime, 'new start before existing end'
        )
        self.assertGreater(
            new_slot.end_datetime, self.slot.end_datetime, 'new end after existing end'
        )

        with self.assertRaises(ValidationError):
            new_slot.safe_save()

    def test_new_slot_end_overlaps(self):
        start_dt = self.slot.start_datetime - timedelta(minutes=10)
        new_slot = BaseSlot(start_datetime=start_dt, duration_in_mins=60)

        self.assertGreater(
            new_slot.end_datetime, self.slot.start_datetime, 'new end after old start'
        )
        self.assertLess(
            new_slot.end_datetime, self.slot.end_datetime, 'new end before old end'
        )
        self.assertLess(
            new_slot.start_datetime, self.slot.start_datetime, 'new start before old start'
        )

        with self.assertRaises(ValidationError):
            new_slot.clean()

    def test_new_slot_in_past(self):
        start_dt = datetime.now() - timedelta(days=1)
        new_slot = BaseSlot(start_datetime=start_dt)

        with self.assertRaises(ValidationError):
            new_slot.clean()

    def test_individual_and_seminar_slots(self):
        common_dt = datetime.now() + timedelta(days=10)

        sem = IndividualSlot(start_datetime=common_dt)
        sem.safe_save()

        ind = IndividualSlot(start_datetime=common_dt)

        with self.assertRaises(ValidationError):
            ind.clean()


class TestSeminarSlots(TestCase):
    '''Test Seminar Specific Functions'''
    def setUp(self):
        # add student
        self.students = {
            'signed_up': Student.objects.create(name='signed_up', email='bob@gmail.com'),
            'awaiting': Student.objects.create(name='awaiting', email='fred@gmail.com'),
            'new': Student.objects.create(name='new', email='new@gmail.com'),
        }

        # add seminar and seminar slot with student
        self.seminar = t_util.create_activity(bookable=True, activity_type="SEM")
        self.slots = t_util.create_seminar_slots(self.seminar)
        self.slots['future'].students.add(self.students['signed_up'])

        # Add awaiting order
        Order.objects.create(
            processor=Order.ProcessorEnums.SEMINAR,
            customer=self.students['awaiting'],
            order_details="example"
        )

    def test_validation_pass(self):
        SeminarSlot.validate_booking(
            slot_id=self.slots['future'].pk,
            student=self.students['new']
        )

    def test_validation_fail_same_student(self):
        with self.assertRaises(ValidationError):
            SeminarSlot.validate_booking(
                slot_id=self.slots['future'].pk,
                student=self.students['signed_up']
            )

    def test_validation_fail_past_seminar(self):
        with self.assertRaises(ValidationError):
            SeminarSlot.validate_booking(
                slot_id=self.slots['past'].pk,
                student=self.students['new']
            )

    def test_validation_fail_not_real_seminar(self):
        with self.assertRaises(ValidationError):
            SeminarSlot.validate_booking(
                slot_id=100210,
                student=self.students['new']
            )
