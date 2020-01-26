'''
A set of conversion functions that will take
in an obj and return an obj of the specified type
'''
import datetime

from . import const


def parse_dt_as_str(datetime_obj):
    '''Converts a `datetime.datetime` to a string
    matching the `FORMAT_LESSON_DATETIME`
    '''
    return datetime_obj.strftime(const.FORMAT_BOOKING_DATETIME)


def parse_str_as_dt(datetime_str):
    '''Converts a `str` to a datetim
    obj using the `FORMAT_LESSON_DATETIME`
    '''
    return datetime.datetime.strptime(
        datetime_str,
        const.FORMAT_BOOKING_DATETIME
    )


def parse_seminar_request(request):
    '''Parse the `Booking` request for the
    expected keys
    '''
    return {sem_key: request[sem_key] for sem_key in const.BOOKING_POST_KEYS}
