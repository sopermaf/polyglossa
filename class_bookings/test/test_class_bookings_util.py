'''This class tests the 'util'
class used by 'class_bookings'
'''
from django.test import TestCase

import class_bookings.util as cb_utils
import class_bookings.data_transform as transform

class TestDataTransform(TestCase): # pylint: disable=missing-class-docstring
    def test_parse_lesson_choice(self):# pylint: disable=missing-function-docstring
        test_input = [
            {
                "exp": "title",
                "in": transform.format_lesson_detail("title", 40),
            },
            {
                "exp": "Medical English",
                "in": transform.format_lesson_detail("Medical English", 40),
            },
        ]

        for data in test_input:
            ret = cb_utils.parse_lesson_choice(data['in'])
            self.assertEqual(data['exp'], ret)
