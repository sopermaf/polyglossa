'''
A suite of validation functions for the class_bookings app
to make sure that requests follow the correct format
'''
import class_bookings.util as cb_utils
from class_bookings.models import Lesson, Student
import datetime


def validate_request(lesson_request):
    '''Validates that the
    `lesson_request` contains all the information
    required.
    '''
    pass


def lesson_unique_time(lesson_time):
    '''Check if lesson time already present

    Args:
    lesson_time -- requested lesson time
    '''
    req_dt = datetime.datetime.strptime(lesson_time, cb_utils.FORMAT_LESSON_DATETIME)
    lessons = Lesson.objects.filter(lesson_datetime=req_dt)
    if lessons:
        raise ValueError(f"{lesson_time} already taken")


def lesson_within_params(lesson_time):
    '''
    '''
    pass


def validate_lesson_request(request_info):
    ''' Perform full validation of lesson request

    Args:
    request_info -- dict of lesson and student data
    '''
    # TODO: cleaning? (whitespace, etc)

    # validation
    lesson_unique_time(request_info[cb_utils.REQUEST_KEY_TIME])
    lesson_within_params(request_info[cb_utils.REQUEST_KEY_TIME])
