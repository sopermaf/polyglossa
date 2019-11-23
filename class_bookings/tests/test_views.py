from django.test import TestCase, Client
import unittest
from django.urls import reverse
from datetime import datetime, timedelta
import class_bookings.util as cb_utils
from class_bookings.models import LessonType, Student, Booking

# TODO:
# 1) POST lesson - ensure it arrives and the response is as expected
# 2) POST Lesson - error occurs and the response is as expected
# 3) POST lesson - student exists
# 4) Move other errors to validation

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.lesson_post_url = reverse(cb_utils.POST_LESSON_URL_NAME)

        # default reFORMAT_BOOKING_DATETIMEf.name = "ferdia"
        self.email = "ferdia@example.com"
        self.name = "bookable lessonType title"
        self.lessonChoice = "available lesson"
        # lesson_datetime only uses HH:MM
        acceptableLessonTimeObj = datetime.now() + cb_utils.MIN_DATETIME_DELTA + timedelta(hours=1)
        self.lesson_datetime_string = cb_utils.convertDateTimeToStr(acceptableLessonTimeObj)
        self.lesson_datetime_obj = cb_utils.convertStrToDateTime(self.lesson_datetime_string)

        # setup DB with an available Lesson
        self.bookableLessonType = LessonType(title=self.lessonChoice, isBookable=True, price=20)
        self.bookableLessonType.save()

    def createBookingParams(self, lesson_slot=None, name=None, email=None, lessonChoice=None):
        booking_params = {}
        if lesson_slot:
            booking_params[cb_utils.REQUEST_KEY_TIME] = lesson_slot
        if name:
            booking_params[cb_utils.REQUEST_KEY_NAME] = name
        if email:
            booking_params[cb_utils.REQUEST_KEY_EMAIL] = email
        if lessonChoice:
            booking_params[cb_utils.REQUEST_KEY_LESSON_CHOICE] = lessonChoice
        return booking_params


    def post_booking(self, booking_params):
        response = self.client.post(
            self.lesson_post_url,
            booking_params
        )
        return response
    

    def post_preset_booking(self):
        booking_params = self.createBookingParams(
            self.lesson_datetime_string,
            self.name,
            self.email,
            self.lessonChoice,
        )
        response = self.post_booking(booking_params)        
        return response


    def test_post_lesson_success(self):
        # make request
        response = self.post_preset_booking()

        # check database now contains data
        self.assertEqual(cb_utils.RESOURCE_CREATED_CODE, response.status_code, "Resource Created Response")
        self.assertEqual(1, len(Booking.objects.all()), "Expect 1 Lesson in DB")
        self.assertEqual(1, len(Student.objects.all()), "Expect 1 Student in DB")

        # assert data added correctly
        lesson = Booking.objects.get(lesson_datetime=self.lesson_datetime_obj)
        self.assertEqual(self.name, lesson.student.name, "Student name should match sent name")
        self.assertEqual(self.email, lesson.student.email, "Student email should match sent email")


    def test_post_lesson_error_missing_data(self):
        # send request
        booking_params = self.createBookingParams(lesson_slot=self.lesson_datetime_string)
        response = self.post_booking(booking_params)
        
        # ensure nothing added and correct code returned
        self.assertEqual(cb_utils.BAD_REQUEST_CODE, response.status_code, "Bad request response expected")
        self.assertEqual(0, len(Booking.objects.all()), "Expected 0 Bookings in DB")
        self.assertEqual(0, len(Student.objects.all()), "Expected 0 Students in DB")


    def test_post_lesson_error_validation(self):
        '''Ensure that the validation is being
        run inside of the POST lesson
        '''
        # make a successful request
        response = self.post_preset_booking()
        self.assertEqual(response.status_code, cb_utils.RESOURCE_CREATED_CODE, "Good Request Response")
        self.assertEqual(1, len(Booking.objects.all()), "Expected 1 Bookings in DB")
        self.assertEqual(1, len(Student.objects.all()), "Expected 1 Students in DB")

        # try to add a second lesson at the same time
        response = self.post_preset_booking()
        self.assertEqual(response.status_code, cb_utils.BAD_REQUEST_CODE, "Bad Request Response")
        self.assertEqual(1, len(Booking.objects.all()), "Expected 1 Bookings in DB")
        self.assertEqual(1, len(Student.objects.all()), "Expected 1 Students in DB")


    def test_post_lesson_existing_student(self):
        # make a successful request
        response = self.post_preset_booking()
        self.assertEqual(response.status_code, cb_utils.RESOURCE_CREATED_CODE, "Good Request Response")
        self.assertEqual(1, len(Booking.objects.all()), "Expected 1 Bookings in DB")
        self.assertEqual(1, len(Student.objects.all()), "Expected 1 Students in DB")

        # make a second request with the same student         
        differentLessonTime = cb_utils.convertDateTimeToStr(
                                self.lesson_datetime_obj + timedelta(days=1)
                              )
        booking_params = self.createBookingParams(
                                                  lesson_slot=differentLessonTime,
                                                  name=self.name,
                                                  email=self.email,
                                                  lessonChoice=self.lessonChoice,
                                                 )
        response = self.post_booking(booking_params)

        # check student not duplicated and second lesson added
        self.assertEqual(response.status_code, cb_utils.RESOURCE_CREATED_CODE, "Good Request Response")
        self.assertEqual(2, len(Booking.objects.all()), "Expected 2 Bookings in DB")
        self.assertEqual(1, len(Student.objects.all()), "Expected 1 Students in DB")

