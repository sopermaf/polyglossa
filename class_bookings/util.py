'''
This file is the central resource for defining
constants and common util functions in class_bookings
'''
import datetime
from django.http import HttpResponse

# request params
REQUEST_KEY_TIME = 'lesson_time'
REQUEST_KEY_NAME = 'student_name'
REQUEST_KEY_EMAIL = 'student_email'
REQUEST_KEY_LESSON_CHOICE = 'lesson_type'
BOOKING_POST_KEYS = [
    REQUEST_KEY_TIME,
    REQUEST_KEY_NAME,
    REQUEST_KEY_EMAIL,
    REQUEST_KEY_LESSON_CHOICE,
]

# HTTP Codes used
BAD_REQUEST_CODE = 400
RESOURCE_CREATED_CODE = 201

# formats
FORMAT_BOOKING_DATETIME = '%Y-%m-%d %H:%M'

# url names
POST_LESSON_URL_NAME = 'create-booking'


# DATETIME FUNCTIONS

def dt_to_str(datetime_obj):
    '''Converts a `datetime.datetime` to a string
    matching the `FORMAT_LESSON_DATETIME`
    '''
    return datetime_obj.strftime(FORMAT_BOOKING_DATETIME)


def str_to_dt(datetime_str):
    '''Converts a `str` to a datetim
    obj using the `FORMAT_LESSON_DATETIME`
    '''
    return datetime.datetime.strptime(
        datetime_str,
        FORMAT_BOOKING_DATETIME
    )


def curr_datetime_str():
    '''Returns a datetime str standard
    format of `datetime.datetime.now()`
    '''
    return dt_to_str(datetime.datetime.now())


# RESPONSES


def http_bad_request(msg="Bad Request"):
    '''Creates a HTTP response
    code `BAD_REQUEST_CODE`
    '''
    error_response = HttpResponse(
        msg,
        status=BAD_REQUEST_CODE,
    )
    return error_response


def http_resource_created(msg="Resource created successfully"):
    '''Returns a HTTP response with code
    `RESOURCE_CREATED_CODE`
    '''
    return HttpResponse(
        msg,
        status=RESOURCE_CREATED_CODE,
    )


# PARSING REQUESTS
# TODO: split into a separate parse file
def parse_post_booking(request):
    '''Parse the `Booking` request for the
    expected keys
    '''
    lesson_request = {}
    for booking_key in BOOKING_POST_KEYS:
        lesson_request[booking_key] = request.POST[booking_key]

    # parse the lesson name
    lesson_request[REQUEST_KEY_LESSON_CHOICE] = parse_lesson_choice(
        lesson_request[REQUEST_KEY_LESSON_CHOICE]
    )

    return lesson_request


def parse_lesson_choice(lesson_choice):
    '''Extracts lesson title from `lesson_choice`
    string from frontend request
    '''
    lesson_title = lesson_choice.split('(')[0]  # format title - ($price)
    cleaned_title = lesson_title.strip()
    return cleaned_title
