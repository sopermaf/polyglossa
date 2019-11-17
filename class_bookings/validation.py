'''
A suite of validation functions for the class_bookings app
to make sure that requests follow the correct format
'''
import class_bookings.util as cb_utils
from class_bookings.models import Lesson, Student
import datetime


def lesson_time_unique(lesson_time):
    '''Check if lesson time already present

    Args:
    `lesson_time` -- str of lesson_time
    '''
    requestedDateTime = datetime.datetime.strptime(
                            lesson_time,
                            cb_utils.FORMAT_LESSON_DATETIME
                        )
    lessons = Lesson.objects.filter(lesson_datetime=requestedDateTime)
    if lessons:
        raise ValueError(f"{lesson_time} already taken")


def lesson_time_within_range(lesson_dt_str):
    '''Check if lesson within allowable
    range of datetimes. Uses max
    and min ranges set in util file.

    Args:
    `lesson_time` -- str of lesson_time
    '''
    currDateTime = datetime.datetime.now()
    lesson_dt_obj = cb_utils.convertStrToDateTime(lesson_dt_str)
    delta_dt_before_lesson = lesson_dt_obj - currDateTime

    if delta_dt_before_lesson > cb_utils.MAX_DATETIME_DELTA:
        raise ValueError(
            "Selected datetime too far away. Max delta {}. Curr delta {}".format(
                cb_utils.MAX_DATETIME_DELTA, delta_dt_before_lesson
            )
        )
    elif delta_dt_before_lesson < cb_utils.MIN_DATETIME_DELTA:
        raise ValueError(
            "Selected datetime too soon. Min delta {}. Curr delta {}".format(
                cb_utils.MIN_DATETIME_DELTA, delta_dt_before_lesson
            )
        )


def validate_lesson_request(request_info):
    ''' Perform full validation of lesson request

    Args:
    request_info -- dict of lesson and student data
    '''
    # TODO: cleaning? (whitespace, etc)

    # validation
    lesson_time_unique(request_info[cb_utils.REQUEST_KEY_TIME])
    lesson_time_within_range(request_info[cb_utils.REQUEST_KEY_TIME])
