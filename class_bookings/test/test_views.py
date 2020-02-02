# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, no-self-use, unused-wildcard-import, wildcard-import

from django.test import TestCase, Client
from django.urls import reverse

from class_bookings.const import *
from class_bookings.models import *
from . import util as t_util


class TestViews(TestCase):
    POST_SEMINAR = reverse(SEMINAR_POST_NAME)

    def setUp(self):
        self.client = Client()
        self.seminar = t_util.create_seminar(bookable=True)
        self.slots = t_util.create_seminar_slots(self.seminar)

    # helper functions

    def create_sem_params(self, *, slot, name, email):
        return {
            KEY_CHOICE: self.slots[slot].id,
            KEY_NAME: name,
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
            slot=self.slots['future'],
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

    def test_seminar_error_validation(self):
        data = self.create_sem_params(
            slot='future', name='joe', email='joe@test.com'
        )
        responses = [self.post_seminar(**data) for i in range(2)]

        # assert status
        self.assertEqual(responses[0].status_code, RESOURCE_CREATED_CODE, 'Success')
        self.assertEqual(responses[1].status_code, BAD_REQUEST_CODE, 'Failure')

        # assert students added
        sem_students = self.slots['future'].students.values()
        self.assertEqual(len(sem_students), 1, 'Only one student added')
