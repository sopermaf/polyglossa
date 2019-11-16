from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime
import class_bookings.util as cb_utils
from class_bookings.models import Lesson, Student

# TODO:
# 1) POST lesson - ensure it arrives and the response is as expected
# 2) POST Lesson - error occurs and the response is as expected
# 3) POST lesson - student exists
# 4) Move other errors to validation

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.lesson_post_url = reverse(cb_utils.POST_LESSON_URL_NAME)
        
        self.lesson_datetime_string = (datetime
                                       .now()
                                       .strftime(
                                        cb_utils
                                        .FORMAT_LESSON_DATETIME
                                        )
                                       )
        self.lesson_post_data = {
            cb_utils.REQUEST_KEY_NAME: 'ferdia',
            cb_utils.REQUEST_KEY_EMAIL: 'ferdia@example.com',
            cb_utils.REQUEST_KEY_TIME: self.lesson_datetime_string,
        }


    def post_preset_lesson(self):
        response = self.client.post(
            self.lesson_post_url,
            self.lesson_post_data,
        )
        return response


    def test_post_lesson_success(self):
        # make request
        response = self.post_preset_lesson()

        # check database for changes
        lesson_datetime = datetime.strptime(
                    self.lesson_datetime_string, 
                    cb_utils.FORMAT_LESSON_DATETIME,
                 )
        lesson = Lesson.objects.get(class_time=lesson_datetime)
        student = lesson.student

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(student.name, self.lesson_post_data[cb_utils.REQUEST_KEY_NAME])
        self.assertEqual(student.email, self.lesson_post_data[cb_utils.REQUEST_KEY_EMAIL])

    # move to validation
    def test_post_lesson_error_missing_data(self):
        '''Post a lesson request resulting
        in an error and ensure no data posted to DB
        and correct response returned
        '''
        # setup
        self.lesson_post_data.pop(cb_utils.REQUEST_KEY_EMAIL)
        response = self.post_preset_lesson()
        
        # check result
        self.assertEqual(response.status_code, cb_utils.BAD_REQUEST_CODE)
        # ensure nothing was added to the database
        self.assertEqual(0, len(Lesson.objects.all()), "Expected 0 Lessons in DB")
        self.assertEqual(0, len(Student.objects.all()), "Expected 0 Students in DB")


    def test_post_lesson_error_validation(self):
        '''Ensure that the validation is being
        run inside of the POST lesson
        '''
        # make a successful request
        response = self.post_preset_lesson()
        self.assertEqual(
            response.status_code,
            cb_utils.RESOURCE_CREATED_CODE,
            "Good Request Response",
            )
        self.assertEqual(1, len(Lesson.objects.all()), "Expected 0 Lessons in DB")
        self.assertEqual(1, len(Student.objects.all()), "Expected 0 Students in DB")

        # make a bad request
        response = self.post_preset_lesson()
        self.assertEqual(
            response.status_code,
            cb_utils.BAD_REQUEST_CODE,
            "Bad Request Response",
            )
        self.assertEqual(1, len(Lesson.objects.all()), "Expected 0 Lessons in DB")
        self.assertEqual(1, len(Student.objects.all()), "Expected 0 Students in DB")



    def test_make_booking_student_exists(self):
        # Ensure the student isn't duplicated
        pass
