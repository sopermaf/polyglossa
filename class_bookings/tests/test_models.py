# pylint: disable=missing-module-docstring
from django.test import TestCase

import class_bookings.models as models
import class_bookings.tests.utils_test as test_utils

class TestModels(TestCase): # pylint: disable=missing-class-docstring
    def setUp(self):    # pylint: disable=missing-function-docstring
        self.lesson_bookable = 'basic bookable lesson'
        self.lesson_not_bookable = "not bookable"

        # DB setup for exisiting LessonType and Student
        test_utils.add_lesson_type_db(self.lesson_bookable, is_bookable=True)
        test_utils.add_lesson_type_db(self.lesson_not_bookable, is_bookable=False)

    def test_get_bookable_titles(self): # pylint: disable=missing-function-docstring
        bookable_lesson_titles = models.LessonType.get_bookable_titles()

        self.assertEqual(len(bookable_lesson_titles), 1, "Expected 1 avail lesson")
        self.assertEqual(
            bookable_lesson_titles[0],
            self.lesson_bookable,
            "Title avail as expected"
        )
