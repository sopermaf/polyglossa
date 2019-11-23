from django.test import TestCase
from datetime import datetime, timedelta
import class_bookings.util as cb_utils
from class_bookings.models import Booking, LessonType, Student
import class_bookings.validation as validation

class TestValidation(TestCase):
    def setUp(self):
        # lesson datetime does not use seconds
        futureTime = datetime.now() + timedelta(days=2)
        self.lesson_datetime_str = cb_utils.convertDateTimeToStr(futureTime)
        self.lesson_datetime_obj = cb_utils.convertStrToDateTime(self.lesson_datetime_str)
        self.name = 'ferdia'
        self.email = 'ferdia@example.com'
        self.nameOfLessonType = 'basic bookable lesson'

        # DB setup for exisiting LessonType and Student
        self.availableLessonType = LessonType(title=self.nameOfLessonType, price=20, isBookable=True)
        self.availableLessonType.save()

        self.student = Student(name=self.name, email=self.email)
        self.student.save()

        # create a booking
        self.booking = Booking(student=self.student,lessonType=self.availableLessonType, lesson_datetime=self.lesson_datetime_obj)
        self.booking.save()

    def test_lesson_time_unique_fail(self):
        with self.assertRaises(ValueError):
            validation.lesson_time_unique(self.lesson_datetime_str)


    def test_lesson_time_unique_pass(self):
        lessonTime = cb_utils.currDateTimeStr()
        validation.lesson_time_unique(lessonTime)


    def test_lesson_time_range_error_max(self):
        lesson_dt_too_far = cb_utils.convertDateTimeToStr(
                    datetime.now() + cb_utils.MAX_DATETIME_DELTA + timedelta(days=1)
                )
        with self.assertRaises(ValueError):
            validation.lesson_time_within_range(lesson_dt_too_far)
    

    def test_lesson_time_range_error_min(self):
        # below min
        lesson_dt_too_soon = cb_utils.convertDateTimeToStr(datetime.now())
        with self.assertRaises(ValueError):
            validation.lesson_time_within_range(lesson_dt_too_soon)

        # before current date
        lesson_dt_negative_delta = cb_utils.convertDateTimeToStr(
                                        datetime.now() - timedelta(days=30)
                                )
        with self.assertRaises(ValueError):
            validation.lesson_time_within_range(lesson_dt_negative_delta)


    def test_lesson_time_range_pass(self):
        # max range
        lesson_dt_max = cb_utils.convertDateTimeToStr(
                                    datetime.now() + cb_utils.MAX_DATETIME_DELTA
                                )
        validation.lesson_time_within_range(lesson_dt_max)

        # min range
        lesson_dt_min = cb_utils.convertDateTimeToStr(
                                        datetime.now() + cb_utils.MIN_DATETIME_DELTA + timedelta(days=1)
                                )
        validation.lesson_time_within_range(lesson_dt_min)
