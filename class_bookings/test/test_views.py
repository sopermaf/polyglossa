# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, no-self-use, unused-wildcard-import, wildcard-import
import json

import pytest
from django.test import TestCase, Client
from django.urls import reverse

from payments.models import Order

from class_bookings.const import *
from class_bookings.models import *
from . import util as t_util
from .. import const


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

        self.slots = t_util.create_seminar_slot_pair(self.activities['SEM']['bookable'])

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
            self.assertEqual(
                resp.status_code,
                const.RESOURCE_CREATED_CODE,
                "Successful Code"
            )

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
        self.assertEqual(
            responses[0].status_code,
            const.RESOURCE_CREATED_CODE,
            'Success'
        )
        self.assertEqual(responses[1].status_code, BAD_REQUEST_CODE, 'Failure')


        self.assertEqual(len(Order.objects.all()), 1, "Single Success Order added")


    def test_get_future_seminar_slots(self):
        response = self.client.get(
            reverse('sem-slots', kwargs={'seminar_id': self.activities['SEM']['bookable'].id})
        )
        self.assertEqual(200, response.status_code, "Successful Request")

        slots = json.loads(response.content)['slots']
        self.assertEqual(1, len(slots), "Single slot returned")
        self.assertEqual(self.slots['future'].id, slots[0]['id'], "Future slot returned")


@pytest.mark.django_db
def test_get_activities(client):
    t_util.create_activity(activity_type=Activity.SEMINAR, order=2)
    t_util.create_activity(activity_type=Activity.SEMINAR, order=1)
    t_util.create_activity(activity_type=Activity.INDIVIDUAL)

    test_cases = [
        (Activity.SEMINAR, 2),
        (Activity.INDIVIDUAL, 1),
        ('NOT REAL', 0),
    ]

    for activity_type, exp_num, in test_cases:
        response = client.get(reverse(
            'get-activities', kwargs={'activity_type': activity_type}
        ))

        # successful request
        assert response.status_code == 200

        # assert data is of expected length and type
        activities = json.loads(response.content)['activities']
        assert len(activities) == exp_num

        # assert ordered and type
        for i, activity in enumerate(activities):
            if i > 0:
                assert activities[i-1]['order_shown'] < activity['order_shown']
            assert activity['activity_type'] == activity_type



@pytest.mark.django_db
def test_get_upcoming_seminars_success(client):
    t_util.create_activity(activity_type=Activity.SEMINAR, title='foo')
    t_util.create_activity(activity_type=Activity.SEMINAR, title='bar')

    tmw = datetime.now() + timedelta(days=1, minutes=10)
    t_util.create_seminar_slot(Activity.objects.get(id=1), tmw)
    t_util.create_seminar_slot(Activity.objects.get(id=2), tmw)

    response = client.get(reverse('get-upcoming-seminars'))
    assert response.status_code == 200

    ret = json.loads(response.content)
    exp = [
        {
            'date': tmw.strftime('%b %d'),
            'seminars': [   # sorted
                'bar',
                'foo',
            ]
        }
    ]

    assert ret == exp


@pytest.mark.django_db
def test_get_upcoming_seminars_date_range(client):
    t_util.create_activity(activity_type=Activity.SEMINAR, title='foo')

    dts = (datetime.now() + timedelta(days=i, minutes=1) for i in range(4, -2, -1))
    t_util.create_seminar_slot(Activity.objects.get(id=1), *dts)

    response = client.get(reverse('get-upcoming-seminars'))
    ret = json.loads(response.content)

    # only today, tmw, and next day shown
    # controlled by views.UPCOMING_TIME_DELTA
    assert len(ret) == 3
    for i, day in enumerate(ret):
        assert day['date'] == (datetime.now() + timedelta(days=i)).strftime('%b %d')


@pytest.mark.django_db
def test_get_upcoming_seminars_unique(client):
    t_util.create_activity(activity_type=Activity.SEMINAR, title='foo')
    seminar = Activity.objects.get(id=1)

    # add 2 slots on same day
    t_util.create_seminar_slot(seminar, (datetime.now() + timedelta(days=1)))
    t_util.create_seminar_slot(seminar, (datetime.now() + timedelta(days=1)))

    response = client.get(reverse('get-upcoming-seminars'))
    ret = json.loads(response.content)

    assert len(ret) == 1    # single day
    assert ret[0]['seminars'] == ['foo']
