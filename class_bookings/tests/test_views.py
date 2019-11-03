from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime
import class_bookings.util as cb
from class_bookings.models import Lesson, Student

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.booking_request = reverse('create-booking')

    def test_make_booking(self):    
        # setup data
        dt_str = datetime.now().strftime(cb.FORMAT_TIME)
        test_name = 'Ferdia'
        test_email = 'ferdia@example.com'

        post_data = {
            cb.REQ_NAME: test_name,
            cb.REQ_EMAIL: test_email,
            cb.REQ_TIME: dt_str,
        }

        # make request
        response = self.client.post(
            reverse(cb.URL_CREATE),
            post_data,
        )
        #print(f"Code: {response.status_code}\nContent:{response.content}")
        #print(f"Full Response: {response}")

        dt_obj = datetime.strptime(dt_str, cb.FORMAT_TIME)
        lesson = Lesson.objects.get(class_time=dt_obj) # throws error
        student = lesson.student

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(student.name, test_name)
        self.assertEqual(student.email, test_email)
