'''
A suite of validation functions for the class_bookings app
to make sure that requests follow the correct format
'''
import class_bookings.util as cb
from class_bookings.models import Lesson, Student
import datetime


def lesson_unique_time(lesson_time):
    '''Check if lesson time already present

    Args:
    lesson_time -- requested lesson time
    '''
    req_dt = datetime.datetime.strptime(lesson_time, cb.FORMAT_TIME)
    lessons = Lesson.objects.filter(class_time=req_dt)
    if lessons:
        raise ValueError(f"{lesson_time} already taken")


def lesson_within_params(lesson_time):
    '''
    '''
    pass


def student_unique_email(name):
    pass


def validate_lesson_request(request_info):
    ''' Perform full validation of lesson request

    Args:
    request_info -- dict of lesson and student data
    '''
    # student validation
    student_unique_email(request_info[cb.REQ_EMAIL])

    # lesson validation
    lesson_unique_time(request_info[cb.REQ_TIME])
    lesson_within_params(request_info[cb.REQ_TIME])
