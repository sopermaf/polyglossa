'''
A suite of validation functions for the class_bookings app
to make sure that requests follow the correct format
'''
import datetime
import class_bookings.util as cb_utils
from class_bookings.models import Booking, LessonType


def booking_datetime_unique(lesson_time):
    '''Check if lesson time already present

    Args:
    `lesson_time` -- str of lesson_time
    '''
    booking_datetime = datetime.datetime.strptime(
        lesson_time,
        cb_utils.FORMAT_BOOKING_DATETIME
    )
    lessons = Booking.objects.filter(lesson_datetime=booking_datetime)  # pylint: disable=no-member
    if lessons:
        raise ValueError(f"{lesson_time} already taken")


def booking_datetime_within_range(lesson_dt_str):
    '''Check if lesson within allowable
    range of datetimes. Uses max
    and min ranges set in util file.

    Args:
    `lesson_time` -- str of lesson_time
    '''
    curr_datetime = datetime.datetime.now()
    lesson_dt_obj = cb_utils.convert_str_to_datetime(lesson_dt_str)
    delta_dt_before_lesson = lesson_dt_obj - curr_datetime

    if delta_dt_before_lesson > cb_utils.MAX_DATETIME_DELTA:
        raise ValueError(
            "Selected datetime too far away. Max delta {}. Curr delta {}".format(
                cb_utils.MAX_DATETIME_DELTA, delta_dt_before_lesson
            )
        )
    if delta_dt_before_lesson < cb_utils.MIN_DATETIME_DELTA:
        raise ValueError(
            "Selected datetime too soon. Min delta {}. Curr delta {}".format(
                cb_utils.MIN_DATETIME_DELTA, delta_dt_before_lesson
            )
        )


def lesson_type_exists(lesson_type_chosen):
    '''Validate that a given lesson
    type exists in the database
    '''
    try:
        LessonType.objects.get(title=lesson_type_chosen)    # pylint: disable=no-member
    except LessonType.DoesNotExist: # pylint: disable=no-member
        raise ValueError(
            f"Lesson type {lesson_type_chosen} doesn't exist"
        )


def lesson_type_bookable(lesson_type_chosen):
    '''Validate that a lesson type is
    available for booking and not restricted
    '''
    lesson = LessonType.objects.get(title=lesson_type_chosen)   # pylint: disable=no-member
    if not lesson.isBookable:
        raise ValueError(
            f'Lesson [{lesson_type_chosen}] not available for booking'
        )


def validate_booking_request(request_info):
    ''' Perform full validation of lesson request

    Args:
    request_info -- dict of lesson and student data
    '''
    booking_datetime = request_info[cb_utils.REQUEST_KEY_TIME]
    lesson_type = request_info[cb_utils.REQUEST_KEY_LESSON_CHOICE]

    # validation
    booking_datetime_unique(booking_datetime)
    booking_datetime_within_range(booking_datetime)
    lesson_type_exists(lesson_type)
    lesson_type_bookable(lesson_type)
