'''
Set of util functions for testing
'''
from uuid import uuid4
from datetime import datetime, timedelta

from class_bookings import models


def create_activity(activity_type, bookable=True, order=1, title=None):
    '''Create a seminar activity'''
    if activity_type not in {models.Activity.INDIVIDUAL, models.Activity.SEMINAR}:
        raise ValueError(f"Invalid activity_type: {activity_type}")

    activity = models.Activity(
        activity_type=activity_type,
        title=title or uuid4(),
        description='description',
        price=20,
        is_bookable=bookable,
        order_shown=order,
    )
    activity.save()
    return activity


def create_seminar_slot_pair(activity):
    """
    Create a future/past slot pair for the given
    `activitiy`.

    Parameter
    ---------
    activitiy : Activity

    Returns
    -------
    dict : 'future' and 'past' seminar slots
    """
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


def create_seminar_slot(activity, *dts):
    '''
    Create a slot for each datetime in `dts`

    Parameters
    ----------
    activity : Activity
    dts      : datetime (of created slot)

    Returns
    -------
    - SeminarSlot
        single datetime given
    - list (SeminarSlots)
        if multiple datetimes provided
    '''
    slots = [
        models.SeminarSlot.objects.create(
            start_datetime=slot_dt,
            seminar=activity
        )
        for slot_dt in dts
    ]

    if len(slots) == 1:
        return slots[0]
    return slots
