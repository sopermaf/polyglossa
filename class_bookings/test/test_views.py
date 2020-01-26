# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from django.test import TestCase, Client
from django.urls import reverse

from class_bookings import const 

# TODO seminar booking test cases
# case 1: normal booking
# case 3: missing data
# case 4: same student
# case 5: seminar not available
# case 5: seminar not real

class TestViews(TestCase):
    POST_URL = reverse(const.SEMINAR_POST_NAME)

    def setUp(self):
        self.client = Client()

    def post_seminar(self, data):
        '''Posts a booking to server with params
        `booking_params` and returns the response
        '''
        response = self.client.post(
            self.POST_URL,
            data=data
        )
        return response

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
