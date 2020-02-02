# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, no-self-use, unused-wildcard-import, wildcard-import

from django.test import TestCase

from class_bookings.const import *
from class_bookings.models import *
from class_bookings.validate import *
from . import util as t_util


class TestValidate(TestCase):
    def setUp(self):
        self.seminar = t_util.create_seminar(bookable=True)
        self.slots = t_util.create_seminar_slots(self.seminar)

        self.student = Student(
            name='joe',
            email='joe@joe.ie'
        )
        self.student.save()

        # add existing student
        self.slots['future'].students.add(self.student)
        self.slots['future'].save()

    # Helper functions

    def create_params(self, *, slot='future', name='bobby',
                      email='bobo@email.ie', use_exisiting=False):
        return {
            KEY_CHOICE: slot if isinstance(slot, int) else self.slots[slot].id,
            KEY_EMAIL: email if not use_exisiting else self.student.email,
            KEY_NAME: name if not use_exisiting else self.student.name,
        }

    # Tests

    def test_validate_seminar_pass(self):
        sem_req = self.create_params()

        # ensure test setup correctly
        self.assertNotEqual(sem_req[KEY_EMAIL], self.student.email, 'Not same email')
        self.assertNotEqual(sem_req[KEY_NAME], self.student.name, 'Not same name')

        validate_seminar_request(sem_req)

    def test_validate_seminar_error_same_student(self):
        sem_req = self.create_params(use_exisiting=True)

        # ensure test setup correctly
        self.assertEqual(sem_req[KEY_EMAIL], self.student.email, 'Same student')
        self.assertEqual(sem_req[KEY_NAME], self.student.name, 'Same student')

        with self.assertRaises(ValueError):
            validate_seminar_request(sem_req)

    def test_validate_seminar_past_date(self):
        sem_req = self.create_params(slot='past')
        with self.assertRaises(ValueError):
            validate_seminar_request(sem_req)

    def test_validate_seminar_not_found(self):
        test_id = -1
        if SeminarSlot.objects.filter(id=test_id):
            raise ValueError(f'Slot with id "{id}" exists')

        sem_req = self.create_params(slot=test_id)
        with self.assertRaises(ValueError):
            validate_seminar_request(sem_req)
