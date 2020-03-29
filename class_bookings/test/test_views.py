# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, no-self-use, unused-wildcard-import, wildcard-import
import json

from django.test import TestCase, Client
from django.urls import reverse

from payments.models import Order

from class_bookings.const import *
from class_bookings.models import *
from . import util as t_util


class TestViews(TestCase):
    POST_SEMINAR = reverse(SEMINAR_POST_NAME)

    def setUp(self):
        self.client = Client()
        self.activities = {
            'SEM': {
                'bookable': t_util.create_activity(activity_type="SEM", bookable=True),
                'not_bookable': t_util.create_activity(activity_type="SEM", bookable=False),
            },
            'IND': {
                'bookable': t_util.create_activity(activity_type="IND", bookable=True),
                'not_bookable': t_util.create_activity(activity_type="IND", bookable=False),
            }
        }

        self.slots = t_util.create_seminar_slots(self.activities['SEM']['bookable'])

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
            self.assertEqual(resp.status_code, 302, "Successful Code")

        # validate in student database
        self.assert_num_db_students(exp_num_students=len(test_students))

        # assert no students added to slots
        for time, slot in self.slots.items():
            self.assertEqual(len(slot.students.values()), 0, f'No Students Added: Sem {time}')

        # assert orders added
        for student in test_students:
            Order.objects.get(customer__name=student[0])


    def test_seminar_missing_data(self):
        required_params = self.create_sem_params(
            slot='future', name='joe', email='joe@test.com'
        )

        # assert requests fail
        for param in required_params:
            send_data = required_params.copy()
            send_data.pop(param)
            response = self.post_seminar(**send_data)
            self.assertEqual(response.status_code, BAD_REQUEST_CODE, 'Failed on missing data')

        # assert no orders added
        self.assertFalse(Order.objects.all(), 'No orders added')


    def test_seminar_error_validation(self):
        data = self.create_sem_params(
            slot='future', name='joe', email='joe@test.com'
        )
        # send two identical requests
        responses = [self.post_seminar(**data) for i in range(2)]

        # assert status
        self.assertEqual(responses[0].status_code, 302, 'Success')
        self.assertEqual(responses[1].status_code, BAD_REQUEST_CODE, 'Failure')

        # TODO: assert single student order added
        self.assertEqual(len(Order.objects.all()), 1, "Single Success Order added")


    def test_get_future_seminar_slots(self):
        response = self.client.get(
            reverse('sem-slots', kwargs={'seminar_id': self.activities['SEM']['bookable'].id})
        )
        self.assertEqual(200, response.status_code, "Successful Request")

        slots = json.loads(response.content)['slots']
        self.assertEqual(1, len(slots), "Single slot returned")
        self.assertEqual(self.slots['future'].id, slots[0]['id'], "Future slot returned")


    def test_get_activities(self):
        test_cases = [
            (Activity.SEMINAR, 1),
            (Activity.INDIVIDUAL, 1),
            ('NOT REAL', 0),
        ]

        for activity_type, exp_num, in test_cases:
            response = self.client.get(reverse(
                'get-activities', kwargs={'activity_type': activity_type}
            ))
            self.assertEqual(200, response.status_code, "SuccessfulRequest")
            activities = json.loads(response.content)['activities']
            self.assertEqual(exp_num, len(activities))
