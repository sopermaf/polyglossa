# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, no-self-use, unused-wildcard-import, wildcard-import
from datetime import datetime, timedelta
from random import random

from django.test import TestCase, Client
from django.urls import reverse

from class_bookings.const import *
from class_bookings.models import *

# TODO seminar booking test cases
# case 1: normal booking
# case 2: missing data
# case 3: same student
# case 4: slot in past
# case 5: slot not real

class TestViews(TestCase):
    POST_SEMINAR = reverse(SEMINAR_POST_NAME)

    def setUp(self):
        self.client = Client()

        self.seminar = self.create_seminar(bookable=True)
        self.sem_slots = {
            'future': SeminarSlot(
                start_datetime=datetime.now() + timedelta(days=1),
                seminar=self.seminar,
            ),
            'past': SeminarSlot(
                seminar=self.seminar,
                start_datetime=datetime.now() - timedelta(days=1),
            )
        }
        for sem in self.sem_slots.values():
            sem.save()

    # helper functions

    def create_seminar(self, *, bookable):
        activity = Activity(
            activity_type=Activity.SEMINAR,
            title='%s' % random(),
            description='%s' % random(),
            price=20,
            is_bookable=bookable,
        )
        activity.save()
        return activity

    def create_sem_params(self, *, slot, name, email):
        return {
            KEY_CHOICE: self.sem_slots[slot].id,
            KEY_STUDENT_NAME: name,
            KEY_EMAIL: email,
        }

    def post_seminar(self, **kwargs):
        response = self.client.post(
            self.POST_SEMINAR,
            data=kwargs
        )
        return response

    def verify_students(self, slot, *, exp_num_students, names, emails):
        students = slot.students.values()
        self.assertEqual(len(students), exp_num_students, "Expected number of students")

        for student, name, email in zip(students, names, emails):
            self.assertEqual(student['name'], name, "Student name correct")
            self.assertEqual(student['email'], email, "Student email correct")

    # Tests

    def test_seminar_success(self):
        data = self.create_sem_params(slot='future', name='joe', email='joe@test.com')
        response = self.post_seminar(**data)

        # lesson code is as expected
        self.assertEqual(response.status_code, RESOURCE_CREATED_CODE, "Successful Code")

        # validate in student database
        students = Student.objects.all()
        self.assertEqual(len(students), 1, "One student Added")

        # validate added to seminar
        self.verify_students(
            slot=self.sem_slots['future'],
            exp_num_students=1,
            names=['joe'],
            emails=['joe@test.com']
        )

    def test_seminar_missing_data(self):
        required_params = {
            KEY_CHOICE: self.sem_slots['future'].id,
            KEY_STUDENT_NAME: 'joe',
            KEY_EMAIL: 'joe@email.com',
        }

        for param in required_params:
            send_data = required_params.copy()
            send_data.pop(param)
            response = self.post_seminar(**send_data)
            self.assertEqual(response.status_code, BAD_REQUEST_CODE, 'Failed on missing data')

    def test_seminar_same_student(self):
        pass

    def test_seminar_error_seminar_id(self):
        pass

    def test_seminar_error_past_seminar(self):
        pass
