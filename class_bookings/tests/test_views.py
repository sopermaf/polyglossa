from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime
import class_bookings.util as cb
from class_bookings.models import Lesson, Student

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.booking_request = reverse(cb.URL_CREATE)
        
        self.datetime_str = datetime.now().strftime(cb.FORMAT_TIME)
        self.post_data = {
            cb.REQ_NAME: 'ferdia',
            cb.REQ_EMAIL: 'ferdia@example.com',
            cb.REQ_TIME: self.datetime_str,
        }


    def post_req(self):
        response = self.client.post(
            self.booking_request,
            self.post_data,
        )
        return response


    def test_make_booking(self):
        # ensure a request works
        # make request
        response = self.post_req()

        # check database for changes
        dt_obj = datetime.strptime(self.datetime_str, cb.FORMAT_TIME)
        lesson = Lesson.objects.get(class_time=dt_obj) # throws error
        student = lesson.student

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(student.name, self.post_data[cb.REQ_NAME])
        self.assertEqual(student.email, self.post_data[cb.REQ_EMAIL])


    def test_lesson_time_clashes(self):
        ''' Ensure the lesson isn't made and correct error returned '''
        # setup first lesson and confirm
        self.post_req()
        lessons = Lesson.objects.all()
        self.assertEqual(len(lessons), 1, "Exactly 1 Lesson in DB")

        with self.assertRaises(ValueError):  # consider changing to specific type
            self.post_req()


    def test_make_booking_missing_data(self):
        # Ensure the request fails
        pass


    def test_make_booking_student_exists(self):
        # Ensure the student isn't duplicated
        pass
