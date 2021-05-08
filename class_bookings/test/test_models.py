# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, no-self-use, wildcard-import

import datetime

import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from class_bookings import errors as err
from class_bookings import models as mods
from . import util as t_util


class TestBaseSlot(TestCase):
    def setUp(self):
        slot_dt = timezone.now() + datetime.timedelta(hours=2)
        self.slot = mods.BaseSlot(start_datetime=slot_dt, duration_in_mins=60)
        self.slot.clean()
        self.slot.save()

    # Tests

    def test_start_at_end_of_slot(self):
        new_slot = mods.BaseSlot(start_datetime=self.slot.end_datetime)
        new_slot.safe_save()

    def test_new_slot_inside_existing(self):
        start_dt = self.slot.start_datetime + datetime.timedelta(minutes=1)
        new_slot = mods.BaseSlot(start_datetime=start_dt, duration_in_mins=5)

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
        start_dt = self.slot.start_datetime - datetime.timedelta(minutes=10)
        new_slot = mods.BaseSlot(start_datetime=start_dt, duration_in_mins=120)

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
        start_dt = self.slot.start_datetime + datetime.timedelta(minutes=10)
        new_slot = mods.BaseSlot(start_datetime=start_dt, duration_in_mins=70)

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
        start_dt = self.slot.start_datetime - datetime.timedelta(minutes=10)
        new_slot = mods.BaseSlot(start_datetime=start_dt, duration_in_mins=60)

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
        start_dt = timezone.now() - datetime.timedelta(days=1)
        new_slot = mods.BaseSlot(start_datetime=start_dt)

        with self.assertRaises(ValidationError):
            new_slot.clean()

    def test_individual_and_seminar_slots(self):
        common_dt = timezone.now() + datetime.timedelta(days=10)

        sem = mods.IndividualSlot(start_datetime=common_dt)
        sem.safe_save()

        ind = mods.IndividualSlot(start_datetime=common_dt)

        with self.assertRaises(ValidationError):
            ind.clean()

    def test_update_existing_slot(self):
        self.slot.duration_in_mins = 30
        self.slot.clean()
        self.slot.save()


@pytest.mark.django_db
def test_validate_signup_error_slot_not_found():
    student = mods.Student(name='foo', email='bar@foo.com')

    # no seminars exist
    with pytest.raises(err.SlotNotFoundError):
        mods.SeminarSlot.validate_signup(1, student)

    # no future seminars exist
    slot = t_util.create_seminar_slot(
        t_util.create_activity(mods.Activity.SEMINAR),
        timezone.now() - datetime.timedelta(days=1)
    )
    with pytest.raises(err.SlotNotFoundError):
        mods.SeminarSlot.validate_signup(slot.id, student)


@pytest.mark.django_db
def test_validate_signup_error_student_present():
    # setup slot with student
    student = mods.Student.objects.create(name='foo', email='bar@foo.com')

    slot = t_util.create_seminar_slot(
        t_util.create_activity(mods.Activity.SEMINAR),
        timezone.now() + datetime.timedelta(days=1)
    )
    slot.students.add(student)
    slot.save()

    with pytest.raises(err.StudentAlreadyPresentError):
        mods.SeminarSlot.validate_signup(slot.id, student)

@pytest.mark.django_db
def test_validate_signup_success():
    # setup slot with student
    student = mods.Student.objects.create(name='foo', email='bar@foo.com')
    slot = t_util.create_seminar_slot(
        t_util.create_activity(mods.Activity.SEMINAR),
        timezone.now() + datetime.timedelta(days=1)
    )


    ret = mods.SeminarSlot.validate_signup(slot.id, student)
    assert isinstance(ret, mods.SeminarSlot)
    assert not slot.students.exists()
