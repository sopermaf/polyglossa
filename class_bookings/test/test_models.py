# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, wildcard-import, unused-wildcard-import
from datetime import datetime, timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError

from class_bookings.models import *

# TODO: test slot range creation tests
# TODO: filter by state where available

class TestSlots(TestCase):
    def setUp(self):
        slot_dt = datetime.now() + timedelta(hours=2)
        self.slot = BaseSlot(start_datetime=slot_dt, duration_in_mins=60)
        self.slot.clean()
        self.slot.save()

    def test_start_at_end_of_slot(self):
        new_slot = BaseSlot(start_datetime=self.slot.end_datetime)
        new_slot.clean()
        new_slot.save()

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
            new_slot.clean()

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
            new_slot.clean()

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
            new_slot.clean()

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
        sem.clean()
        sem.save()

        ind = IndividualSlot(start_datetime=common_dt)

        with self.assertRaises(ValidationError):
            ind.clean()
