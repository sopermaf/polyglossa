# pylint: disable=missing-module-docstring
from datetime import datetime, timedelta
from django.test import TestCase
import class_bookings.util as cb_utils
from class_bookings.models import Booking, LessonType, Student
import class_bookings.validation as validation

class TestValidation(TestCase): # pylint: disable=missing-class-docstring
    @staticmethod
    def add_lesson_type_db(title, is_bookable):
        '''Add a lesson to test DB
        '''
        lesson_type = LessonType(
            title=title,
            price=20,
            isBookable=is_bookable,
        )
        lesson_type.save()


    def setUp(self):    # pylint: disable=missing-function-docstring
        # lesson datetime does not use seconds
        future_datetime = datetime.now() + timedelta(days=2)
        self.lesson_datetime_str = cb_utils.convert_datetime_to_str(future_datetime)
        self.lesson_datetime_obj = cb_utils.convert_str_to_datetime(self.lesson_datetime_str)
        self.name = 'ferdia'
        self.email = 'ferdia@example.com'
        self.lesson_bookable = 'basic bookable lesson'
        self.lesson_not_bookable = "not bookable"

        # DB setup for exisiting LessonType and Student
        TestValidation.add_lesson_type_db(self.lesson_bookable, is_bookable=True)
        TestValidation.add_lesson_type_db(self.lesson_not_bookable, is_bookable=False)

        student = Student(name=self.name, email=self.email)
        student.save()

        # create a booking
        self.booking = Booking(
            student=student,
            lessonType=LessonType.objects.get(title=self.lesson_bookable), # pylint: disable=no-member
            lesson_datetime=self.lesson_datetime_obj
        )
        self.booking.save()


    def test_lesson_time_unique_fail(self): # pylint: disable=missing-function-docstring
        with self.assertRaises(ValueError):
            validation.booking_datetime_unique(self.lesson_datetime_str)


    @staticmethod
    def test_lesson_time_unique_pass(): # pylint: disable=missing-function-docstring
        booking_time = cb_utils.curr_datetime_str()
        validation.booking_datetime_unique(booking_time)


    def test_lesson_time_range_error_max(self): # pylint: disable=missing-function-docstring
        lesson_dt_too_far = cb_utils.convert_datetime_to_str(
            datetime.now() + cb_utils.MAX_DATETIME_DELTA + timedelta(days=1)
        )
        with self.assertRaises(ValueError):
            validation.booking_datetime_within_range(lesson_dt_too_far)


    def test_lesson_time_range_error_min(self): # pylint: disable=missing-function-docstring
        # below min
        lesson_dt_too_soon = cb_utils.convert_datetime_to_str(datetime.now())
        with self.assertRaises(ValueError):
            validation.booking_datetime_within_range(lesson_dt_too_soon)

        # before current date
        lesson_dt_negative_delta = cb_utils.convert_datetime_to_str(
            datetime.now() - timedelta(days=30)
        )
        with self.assertRaises(ValueError):
            validation.booking_datetime_within_range(lesson_dt_negative_delta)


    @staticmethod
    def test_lesson_time_range_pass():  # pylint: disable=missing-function-docstring
        booking_max_datetime = cb_utils.convert_datetime_to_str(
            datetime.now() + cb_utils.MAX_DATETIME_DELTA
        )
        validation.booking_datetime_within_range(booking_max_datetime)

        booking_min_datetime = cb_utils.convert_datetime_to_str(
            datetime.now() + cb_utils.MIN_DATETIME_DELTA + timedelta(days=1)
        )
        validation.booking_datetime_within_range(booking_min_datetime)


    def test_lesson_type_exists_pass(self): # pylint: disable=missing-function-docstring
        validation.lesson_type_exists(self.lesson_bookable)


    def test_lesson_type_exists_fail(self): # pylint: disable=missing-function-docstring
        with self.assertRaises(ValueError):
            validation.lesson_type_exists("NOT REAL LESSON TYPE")


    def test_lesson_bookable_pass(self): # pylint: disable=missing-function-docstring
        validation.lesson_type_bookable(self.lesson_bookable)


    def test_lesson_bookable_fail(self): # pylint: disable=missing-function-docstring
        with self.assertRaises(ValueError):
            validation.lesson_type_bookable(self.lesson_not_bookable)
