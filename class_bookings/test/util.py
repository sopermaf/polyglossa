'''
Set of util functions for testing
'''
from random import random
from datetime import datetime, timedelta

from class_bookings import models

def create_seminar(*, bookable):
    '''Create a seminar activity'''
    activity = models.Activity(
        activity_type=models.Activity.SEMINAR,
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
