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

    def verify_students(self, slot, *, student_data):
        students = slot.students.values()
        self.assertEqual(len(students), len(student_data), "Expected number of students")

        for student, test in zip(students, student_data):
            self.assertEqual(student['name'], test[0], "Student name correct")
            self.assertEqual(student['email'], test[1], "Student email correct")

    def assert_num_db_students(self, *, exp_num_students):
        students = Student.objects.all()
        self.assertEqual(
            len(students), exp_num_students, f"Expected {exp_num_students} students"
        )

    # Tests

    def test_seminar_success(self):
        test_students = [('joe', 'joe@test.com'), ('fred', 'fred@test.com')]
        data = [
            self.create_sem_params(slot='future', name=s[0], email=s[1])
            for s in test_students
        ]
        responses = [self.post_seminar(**d) for d in data]

        # assert status code
        for resp in responses:
            self.assertEqual(resp.status_code, RESOURCE_CREATED_CODE, "Successful Code")

        # validate in student database
        self.assert_num_db_students(exp_num_students=len(test_students))

        # validate added to seminar
        self.verify_students(
            slot=self.sem_slots['future'],
            student_data=test_students
        )

    def test_seminar_missing_data(self):
        required_params = self.create_sem_params(
            slot='future', name='joe', email='joe@test.com'
        )

        for param in required_params:
            send_data = required_params.copy()
            send_data.pop(param)
            response = self.post_seminar(**send_data)
            self.assertEqual(response.status_code, BAD_REQUEST_CODE, 'Failed on missing data')

    def test_seminar_error_same_student(self):
        data = self.create_sem_params(
            slot='future', name='joe', email='joe@test.com'
        )
        responses = [self.post_seminar(**data) for i in range(2)]

        # assert status
        self.assertEqual(responses[0].status_code, RESOURCE_CREATED_CODE, 'Success')
        self.assertEqual(responses[1].status_code, BAD_REQUEST_CODE, 'Failure')

        # assert students added
        sem_students = self.sem_slots['future'].students.values()
        self.assertEqual(len(sem_students), 1, 'Only one student added')

    def test_seminar_error_seminar_id(self):
        data = {
            KEY_CHOICE: 100,
            KEY_STUDENT_NAME: 'joe',
            KEY_EMAIL: 'joe@test.ie',
        }
        response = self.post_seminar(**data)

        self.assertEqual(len(SeminarSlot.objects.filter(id=data[KEY_CHOICE])), 0, 'Slot not real')
        self.assertEqual(response.status_code, BAD_REQUEST_CODE, 'Request failed')
        self.assert_num_db_students(exp_num_students=0)

    def test_seminar_error_past_seminar(self):
        data = self.create_sem_params(slot='past', name='joe', email='joe@test.ie')
        response = self.post_seminar(**data)

        self.assertEqual(response.status_code, BAD_REQUEST_CODE, "Request Failed")
        self.assert_num_db_students(exp_num_students=0)
