# pylint: disable=missing-module-docstring
from django.test import TestCase

import class_bookings.tests.utils_test as test_utils
import class_bookings.data_transform as transform

class TestDataTransform(TestCase): # pylint: disable=missing-class-docstring
    def setUp(self):    # pylint: disable=missing-function-docstring
        self.lesson_bookable = 'basic bookable lesson'
        self.lesson_not_bookable = "not bookable"
        self.bookable_price = 20

        # DB setup for exisiting LessonType and Student
        test_utils.add_lesson_type_db(
            self.lesson_bookable,
            is_bookable=True,
            price=self.bookable_price
        )
        test_utils.add_lesson_type_db(self.lesson_not_bookable, is_bookable=False)

    def test_get_bookable_titles(self): # pylint: disable=missing-function-docstring
        bookable_lesson_details = transform.get_bookable_lesson_details()
        expected_bookable = "%s (USD$%.2f)" % (self.lesson_bookable, self.bookable_price)

        self.assertEqual(len(bookable_lesson_details), 1, "Expected 1 bookable lesson")
        self.assertEqual(
            bookable_lesson_details[0],
            expected_bookable,
            "Title and Price format as expected"
        )
