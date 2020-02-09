'''
Set of util functions for testing
'''
from random import random
from datetime import datetime, timedelta

from class_bookings import models


def create_activity(*, activity_type, bookable):
    '''Create a seminar activity'''
    if activity_type not in {models.Activity.INDIVIDUAL, models.Activity.SEMINAR}:
        raise ValueError(f"Invalid activity_type: {activity_type}")

    activity = models.Activity(
        activity_type=activity_type,
        title='%s' % random(),
        description='%s' % random(),
        price=20,
        is_bookable=bookable,
    )
    activity.save()
    return activity


def create_seminar_slots(activity):
    '''Returns a dict containing
    a `future` and `past` seminar slot for testing
    using the activity set
    '''
    slots = {
        'future': models.SeminarSlot(
            start_datetime=datetime.now() + timedelta(days=1),
            seminar=activity,
        ),
        'past': models.SeminarSlot(
            seminar=activity,
            start_datetime=datetime.now() - timedelta(days=1),
        )
    }
    for slot in slots.values():
        slot.save()
    return slots
