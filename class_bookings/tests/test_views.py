from django.test import TestCase, Client
import unittest
from django.urls import reverse
from datetime import datetime, timedelta
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

        self.name = "ferdia"
        self.email = "ferdia@example.com"

        # lesson_datetime only uses HH:MM
        self.lesson_datetime_string = datetime.now().strftime(cb_utils.FORMAT_LESSON_DATETIME)
        self.lesson_datetime_obj = datetime.strptime(
                                    self.lesson_datetime_string,
                                    cb_utils.FORMAT_LESSON_DATETIME
                                )

    def post_preset_lesson(self, name=None, email=None, lessonTime=None, default=False):
        '''Posts a lesson to the server.
        Uses default values if `default` is true
        '''
        if default:
            name = self.name
            email = self.email
            lessonTime = self.lesson_datetime_string

        lesson_post_data = {
            cb_utils.REQUEST_KEY_NAME: name,
            cb_utils.REQUEST_KEY_EMAIL: email,
            cb_utils.REQUEST_KEY_TIME: lessonTime,
        }

        response = self.client.post(
            self.lesson_post_url,
            lesson_post_data
        )
        return response


    def test_post_lesson_success(self):
        # make request
        response = self.post_preset_lesson(default=True)

        # check database now contains data
        self.assertEqual(cb_utils.RESOURCE_CREATED_CODE, response.status_code, "Resource Created Response")
        self.assertEqual(1, len(Lesson.objects.all()), "Expect 1 Lesson in DB")
        self.assertEqual(1, len(Student.objects.all()), "Expect 1 Student in DB")

        # assert data added correctly
        lesson = Lesson.objects.get(class_time=self.lesson_datetime_obj)
        self.assertEqual(self.name, lesson.student.name, "Student name should match sent name")
        self.assertEqual(self.email, lesson.student.email, "Student email should match sent email")


    @unittest.skip("wip")
    def test_post_lesson_error_missing_data(self):
        '''Post a lesson request resulting
        in an error and ensure no data posted to DB
        and correct response returned
        '''
        # setup
        self.lesson_post_data.pop(cb_utils.REQUEST_KEY_EMAIL)
        response = self.post_preset_lesson()
        
        # check result
        self.assertEqual(cb_utils.BAD_REQUEST_CODE, response.status_code, "Bad request response expected")
        # ensure nothing was added to the database
        self.assertEqual(0, len(Lesson.objects.all()), "Expected 0 Lessons in DB")
        self.assertEqual(0, len(Student.objects.all()), "Expected 0 Students in DB")

    @unittest.skip("wip")
    def test_post_lesson_error_validation(self):
        '''Ensure that the validation is being
        run inside of the POST lesson
        '''
        # make a successful request
        response = self.post_preset_lesson()
        self.assertEqual(response.status_code, cb_utils.RESOURCE_CREATED_CODE, "Good Request Response")
        self.assertEqual(1, len(Lesson.objects.all()), "Expected 1 Lessons in DB")
        self.assertEqual(1, len(Student.objects.all()), "Expected 1 Students in DB")

        # make a bad request
        response = self.post_preset_lesson()
        self.assertEqual(response.status_code, cb_utils.BAD_REQUEST_CODE,"Bad Request Response",
            )
        self.assertEqual(1, len(Lesson.objects.all()), "Expected 1 Lessons in DB")
        self.assertEqual(1, len(Student.objects.all()), "Expected 1 Students in DB")


    @unittest.skip("wip")
    def test_make_booking_student_exists(self):
        '''Ensure the student isn't duplicated
        on their second request.
        '''
        response = self.post_preset_lesson()
        self.assertEqual(response.status_code, cb_utils.RESOURCE_CREATED_CODE, "Good Request Response")
        self.assertEqual(1, len(Lesson.objects.all()), "Expected 1 Lessons in DB")
        self.assertEqual(1, len(Student.objects.all()), "Expected 1 Students in DB")

        # new time, same student            
        tomorrowDateTimeObj = datetime.now() + timedelta(days=1)            

        self.lesson_datetime_string = tomorrowDateTimeObj.strftime(cb_utils.FORMAT_LESSON_DATETIME)
        
        response = self.post_preset_lesson()
        #self.assertEqual(response.status_code, cb_utils.RESOURCE_CREATED_CODE, "Good Request Response")
        self.assertEqual(2, len(Lesson.objects.all()), "Expected 2 Lessons in DB")
        self.assertEqual(1, len(Student.objects.all()), "Expected 1 Students in DB")

