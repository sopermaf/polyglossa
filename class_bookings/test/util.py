'''
Set of util functions for testing
'''
from uuid import uuid4
import datetime

from django.utils import timezone

from class_bookings.models import Activity, SeminarSlot


def create_activity(activity_type=Activity.SEMINAR, bookable=True, order=1, title=None, price=20):
    '''Create a seminar activity'''
    if activity_type not in {Activity.INDIVIDUAL, Activity.SEMINAR}:
        raise ValueError(f"Invalid activity_type: {activity_type}")

    activity = Activity(
        activity_type=activity_type,
        title=title or uuid4(),
        description='description',
        price=price,
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
    future = SeminarSlot.objects.create(
        start_datetime=timezone.now() + datetime.timedelta(days=1),
        seminar=activity,
    )
    past = SeminarSlot.objects.create(
        start_datetime=timezone.now() - datetime.timedelta(days=1),
        seminar=activity,
    )
    return {
        'future': future,
        'past': past,
    }


def create_seminar_slot(activity, *dts, video_id='video_id',):
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
        SeminarSlot.objects.create(
            start_datetime=slot_dt,
            seminar=activity,
            video_id=video_id,
        )
        for slot_dt in dts
    ]

    if len(slots) == 1:
        return slots[0]
    return slots
