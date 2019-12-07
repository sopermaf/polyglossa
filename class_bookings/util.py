'''
This file is the central resource for defining
constants and common util functions in class_bookings
'''
import datetime
from django.http import HttpResponse

# LIMITS
MAX_DATETIME_DELTA = datetime.timedelta(days=30)
MIN_DATETIME_DELTA = datetime.timedelta(hours=12)

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

def convert_datetime_to_str(datetime_obj):
    '''Converts a `datetime.datetime` to a string
    matching the `FORMAT_LESSON_DATETIME`
    '''
    return datetime_obj.strftime(FORMAT_BOOKING_DATETIME)


def convert_str_to_datetime(datetime_str):
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
    return convert_datetime_to_str(datetime.datetime.now())


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
