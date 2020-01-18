# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from django.test import TestCase, Client
from django.urls import reverse

import class_bookings.util as cb_utils


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.lesson_post_url = reverse(cb_utils.POST_LESSON_URL_NAME)

        # add activities to db for retrieval

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

    # TODO: fix with new Activity model
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

    # TODO: implement with new models
    def test_post_lesson_success(self):
        pass

    # TODO: implement with new models
    def test_post_lesson_error_missing_data(self):
        pass

    # TODO: implement with new models
    def test_post_lesson_error_validation(self):
        pass

    # TODO: implement with new models
    def test_post_booking_with_same_student(self):
        pass
