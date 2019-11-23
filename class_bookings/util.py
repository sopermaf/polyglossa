'''
This file is the central resource for defining 
constants and common util functions in class_bookings
'''
import datetime

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


def convertDateTimeToStr(datetimeObj):
    '''Converts a `datetime.datetime` to a string
    matching the `FORMAT_LESSON_DATETIME`
    '''
    return datetimeObj.strftime(FORMAT_BOOKING_DATETIME)


def convertStrToDateTime(datetimeStr):
    '''Converts a `str` to a datetim
    obj using the `FORMAT_LESSON_DATETIME`
    '''
    return datetime.datetime.strptime(
                            datetimeStr,
                            FORMAT_BOOKING_DATETIME
                        )


def currDateTimeStr():
    '''Returns a datetime str standard
    format of `datetime.datetime.now()`
    '''
    return convertDateTimeToStr(datetime.datetime.now())
