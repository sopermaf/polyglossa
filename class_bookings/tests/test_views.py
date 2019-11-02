from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime

class TestViews(TestCase):
    def setup(self):
        self.client = Client()
        self.booking_request = reverse('create-booking')

    def test_make_booking(self):    
        # setup data
        datetime_pattern = '%Y-%m-%d %H:%M'
        dt = datetime.now().strftime(datetime_pattern)
        
        post_data = {
            'student_name': 'Ferdia',
            'student_email': 'ferdia@example.com',
            'lesson_time': dt,
        }

        # make request
        response = self.client.post(
            reverse('create-booking'),
            post_data,
        )
        print(f"Code: {response.status_code}\nContent:{response.content}")
        print(f"Full Response: {response}")

        # assert
        self.assertEqual(response.status_code, 200)
        # confirm that the student was saved in the DB after the request