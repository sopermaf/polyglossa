# pylint: disable=missing-module-docstring
from datetime import datetime, timedelta
from django.test import TestCase
import class_bookings.util as cb_utils
from class_bookings.models import Booking, LessonType, Student
import class_bookings.validation as validation

class TestValidation(TestCase): # pylint: disable=missing-class-docstring
    def setUp(self):    # pylint: disable=missing-function-docstring
        # lesson datetime does not use seconds
        future_datetime = datetime.now() + timedelta(days=2)
        self.lesson_datetime_str = cb_utils.convert_datetime_to_str(future_datetime)
        self.lesson_datetime_obj = cb_utils.convert_str_to_datetime(self.lesson_datetime_str)
        self.name = 'ferdia'
        self.email = 'ferdia@example.com'
        self.lesson_type_title = 'basic bookable lesson'

        # DB setup for exisiting LessonType and Student
        available_lesson_type = LessonType(
            title=self.lesson_type_title,
            price=20,
            isBookable=True
        )
        available_lesson_type.save()

        self.student = Student(name=self.name, email=self.email)
        self.student.save()

        # create a booking
        self.booking = Booking(
            student=self.student,
            lessonType=available_lesson_type,
            lesson_datetime=self.lesson_datetime_obj
        )
        self.booking.save()

    def test_lesson_time_unique_fail(self): # pylint: disable=missing-function-docstring
        with self.assertRaises(ValueError):
            validation.lesson_time_unique(self.lesson_datetime_str)

    @staticmethod
    def test_lesson_time_unique_pass(): # pylint: disable=missing-function-docstring
        booking_time = cb_utils.curr_datetime_str()
        validation.lesson_time_unique(booking_time)


    def test_lesson_time_range_error_max(self): # pylint: disable=missing-function-docstring
        lesson_dt_too_far = cb_utils.convert_datetime_to_str(
            datetime.now() + cb_utils.MAX_DATETIME_DELTA + timedelta(days=1)
        )
        with self.assertRaises(ValueError):
            validation.lesson_time_within_range(lesson_dt_too_far)


    def test_lesson_time_range_error_min(self): # pylint: disable=missing-function-docstring
        # below min
        lesson_dt_too_soon = cb_utils.convert_datetime_to_str(datetime.now())
        with self.assertRaises(ValueError):
            validation.lesson_time_within_range(lesson_dt_too_soon)

        # before current date
        lesson_dt_negative_delta = cb_utils.convert_datetime_to_str(
            datetime.now() - timedelta(days=30)
        )
        with self.assertRaises(ValueError):
            validation.lesson_time_within_range(lesson_dt_negative_delta)

    @staticmethod
    def test_lesson_time_range_pass():  # pylint: disable=missing-function-docstring
        booking_max_datetime = cb_utils.convert_datetime_to_str(
            datetime.now() + cb_utils.MAX_DATETIME_DELTA
        )
        validation.lesson_time_within_range(booking_max_datetime)

        booking_min_datetime = cb_utils.convert_datetime_to_str(
            datetime.now() + cb_utils.MIN_DATETIME_DELTA + timedelta(days=1)
        )
        validation.lesson_time_within_range(booking_min_datetime)
