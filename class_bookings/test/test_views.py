# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from datetime import datetime, timedelta
from random import random

from django.test import TestCase, Client
from django.urls import reverse

from class_bookings.const import * 
from class_bookings.models import * 

# TODO seminar booking test cases
# case 1: normal booking
# case 3: missing data
# case 4: same student
# case 5: slot in past
# case 5: slot not real

class TestViews(TestCase):
    POST_SEMINAR = reverse(SEMINAR_POST_NAME)

    def setUp(self):
        self.client = Client()
        self.seminars = {
            'avail': self.create_seminar(bookable=True),
            'unavail': self.create_seminar(bookable=False),
        }
        self.sem_slot = SeminarSlot(
            start_datetime=datetime.now() + timedelta(days=1),
            seminar=self.seminars['avail'],
        )
        self.sem_slot.safe_save()
        
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


    def post_seminar(self, **kwargs):
        print(kwargs)
        response = self.client.post(
            self.POST_SEMINAR,
            data=kwargs
        )
        return response


    def test_seminar_success(self):
        response = self.post_seminar(
            **{
                KEY_CHOICE: self.sem_slot.id,
                KEY_EMAIL: 'joe@test.com',
                KEY_STUDENT_NAME: 'joe',
            }
        )

        self.assertEqual(response.status_code, RESOURCE_CREATED_CODE, "Successful Code")

        students = Student.objects.all()
        self.assertEqual(len(students), 1, "Single Student Created")
        self.assertEqual(students[0].name, "joe", "Student name correct")
        self.assertEqual(students[0].email, "joe@test.com", "Student email correct")

        sem_slot_students = self.sem_slot.students.values()
        self.assertEqual(len(sem_slot_students), 1, "Student added")

