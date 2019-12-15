# pylint: disable=missing-module-docstring
from datetime import datetime, timedelta
from django.test import TestCase, Client
from django.urls import reverse

import class_bookings.util as cb_utils
import class_bookings.data_transform as transform
from class_bookings.models import LessonType, Student, Booking


class TestViews(TestCase): # pylint: disable=missing-class-docstring
    def setUp(self):    # pylint: disable=no-member, missing-function-docstring
        self.client = Client()
        self.lesson_post_url = reverse(cb_utils.POST_LESSON_URL_NAME)

        self.email = "ferdia@example.com"
        self.name = "bookable lessonType title"
        self.lesson_type_title = "available lesson"


        # lesson_datetime only uses HH:MM
        self.lesson_datetime_string = cb_utils.convert_datetime_to_str(
            datetime.now() + cb_utils.MIN_DATETIME_DELTA + timedelta(hours=1)
        )
        self.lesson_datetime_obj = cb_utils.convert_str_to_datetime(self.lesson_datetime_string)

        # setup DB with an available Lesson
        lesson_type = LessonType(
            title=self.lesson_type_title,
            isBookable=True,
            price=20
        )
        lesson_type.save()
        self.lesson_type_title = transform.format_lesson_detail(self.lesson_type_title, 20)

    @staticmethod
    def create_booking_parms(lesson_slot=None, name=None, email=None, lesson_type=None):
        '''Generate the params for a POST booking request
        '''
        booking_params = {}
        if lesson_slot:
            booking_params[cb_utils.REQUEST_KEY_TIME] = lesson_slot
        if name:
            booking_params[cb_utils.REQUEST_KEY_NAME] = name
        if email:
            booking_params[cb_utils.REQUEST_KEY_EMAIL] = email
        if lesson_type:
            booking_params[cb_utils.REQUEST_KEY_LESSON_CHOICE] = lesson_type
        return booking_params


    def post_booking(self, booking_params):
        '''Posts a booking to server with params
        `booking_params` and returns the response
        '''
        response = self.client.post(
            self.lesson_post_url,
            booking_params
        )
        return response


    def post_preset_booking(self):
        '''Post a booking to the server
        using the default settings from `setup`
        '''
        booking_params = self.create_booking_parms(
            self.lesson_datetime_string,
            self.name,
            self.email,
            self.lesson_type_title,
        )
        response = self.post_booking(booking_params)
        return response


    def test_post_lesson_success(self):     # pylint: disable=missing-function-docstring
        response = self.post_preset_booking()

        self.assertEqual(cb_utils.RESOURCE_CREATED_CODE, response.status_code, "Success code")
        self.assertEqual(1, len(Booking.objects.all()), "Expect 1 Booking in DB")    # pylint: disable=no-member
        self.assertEqual(1, len(Student.objects.all()), "Expect 1 Student in DB")   # pylint: disable=no-member

        lesson = Booking.objects.get(lesson_datetime=self.lesson_datetime_obj)  # pylint: disable=no-member
        self.assertEqual(self.name, lesson.student.name, "Student name should match sent name")
        self.assertEqual(self.email, lesson.student.email, "Student email should match sent email")


    def test_post_lesson_error_missing_data(self):  # pylint: disable=missing-function-docstring
        booking_params = self.create_booking_parms(lesson_slot=self.lesson_datetime_string)
        response = self.post_booking(booking_params)

        self.assertEqual(cb_utils.BAD_REQUEST_CODE, response.status_code, "Failure code")
        self.assertEqual(0, len(Booking.objects.all()), "Expected 0 Bookings in DB")    # pylint: disable=no-member
        self.assertEqual(0, len(Student.objects.all()), "Expected 0 Students in DB")    # pylint: disable=no-member


    def test_post_lesson_error_validation(self):    # pylint: disable=missing-function-docstring
        '''Ensure that the validation is being
        run inside of the POST lesson
        '''
        # make a successful request
        response = self.post_preset_booking()
        self.assertEqual(response.status_code, cb_utils.RESOURCE_CREATED_CODE, "Success code")
        self.assertEqual(1, len(Booking.objects.all()), "Expected 1 Bookings in DB")    # pylint: disable=no-member
        self.assertEqual(1, len(Student.objects.all()), "Expected 1 Students in DB")    # pylint: disable=no-member

        # try to add a second lesson at the same time
        response = self.post_preset_booking()
        self.assertEqual(response.status_code, cb_utils.BAD_REQUEST_CODE, "Failure code")
        self.assertEqual(1, len(Booking.objects.all()), "Expected 1 Bookings in DB")    # pylint: disable=no-member
        self.assertEqual(1, len(Student.objects.all()), "Expected 1 Students in DB")    # pylint: disable=no-member


    def test_post_booking_with_same_student(self):  # pylint: disable=missing-function-docstring
        # make a successful request
        response = self.post_preset_booking()
        self.assertEqual(response.status_code, cb_utils.RESOURCE_CREATED_CODE, "Success Code")
        self.assertEqual(1, len(Booking.objects.all()), "Expected 1 Bookings in DB")    # pylint: disable=no-member
        self.assertEqual(1, len(Student.objects.all()), "Expected 1 Students in DB")    # pylint: disable=no-member

        new_booking_datetime = cb_utils.convert_datetime_to_str(
            self.lesson_datetime_obj + timedelta(days=1)
        )
        booking_params = self.create_booking_parms(
            lesson_slot=new_booking_datetime,
            name=self.name,
            email=self.email,
            lesson_type=self.lesson_type_title,
        )
        response = self.post_booking(booking_params)

        # check student not duplicated and second lesson added
        self.assertEqual(response.status_code, cb_utils.RESOURCE_CREATED_CODE, "Success Code")
        self.assertEqual(2, len(Booking.objects.all()), "Expected 2 Bookings in DB")    # pylint: disable=no-member
        self.assertEqual(1, len(Student.objects.all()), "Expected 1 Students in DB")    # pylint: disable=no-member
