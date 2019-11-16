from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime
import class_bookings.util as class_booking_utils
from class_bookings.models import Lesson, Student

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.lesson_post_url = reverse(class_booking_utils.POST_LESSON_URL_NAME)
        
        self.lesson_datetime_string = (datetime
                                       .now()
                                       .strftime(
                                        class_booking_utils
                                        .FORMAT_LESSON_DATETIME
                                        )
                                       )
        self.lesson_post_data = {
            class_booking_utils.REQUEST_KEY_NAME: 'ferdia',
            class_booking_utils.REQUEST_KEY_EMAIL: 'ferdia@example.com',
            class_booking_utils.REQUEST_KEY_TIME: self.lesson_datetime_string,
        }


    def post_preset_lesson(self):
        response = self.client.post(
            self.lesson_post_url,
            self.lesson_post_data,
        )
        return response


    def test_post_lesson(self):
        # make request
        response = self.post_preset_lesson()

        # check database for changes
        lesson_datetime = datetime.strptime(
                    self.lesson_datetime_string, 
                    class_booking_utils.FORMAT_LESSON_DATETIME,
                 )
        lesson = Lesson.objects.get(class_time=lesson_datetime)
        student = lesson.student

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(student.name, self.lesson_post_data[class_booking_utils.REQUEST_KEY_NAME])
        self.assertEqual(student.email, self.lesson_post_data[class_booking_utils.REQUEST_KEY_EMAIL])


    def test_lesson_time_clashes(self):
        ''' Ensure the lesson isn't made and correct error returned '''
        # setup first lesson and confirm
        self.post_preset_lesson()
        lessons = Lesson.objects.all()
        self.assertEqual(len(lessons), 1, "Exactly 1 Lesson in DB")

        with self.assertRaises(ValueError):  # consider changing to specific type
            self.post_preset_lesson()


    def test_make_booking_missing_data(self):
        # Ensure the request fails
        pass


    def test_make_booking_student_exists(self):
        # Ensure the student isn't duplicated
        pass
