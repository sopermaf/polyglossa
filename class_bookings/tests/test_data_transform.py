# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from django.test import TestCase

import class_bookings.data_transform as transform


class TestDataTransform(TestCase):
    def setUp(self):
        self.lesson_bookable = 'basic bookable lesson'
        self.lesson_not_bookable = "not bookable"
        self.bookable_price = 20

        # DB setup for exisiting LessonType and Student
        # TODO: setup a bookable lesson and unbookable

    def test_format_lesson_detail(self):
        price = 20
        title = "title title"
        expected_output = "title title (USD$20.00)"

        self.assertEqual(
            expected_output, transform.format_lesson_detail(title, price))

    # TODO: implement with new models
    def test_get_bookable_titles(self):
        pass
