'''
Validation functions for requests
'''
from datetime import datetime

from . import const
from .models import SeminarSlot


def validate_seminar_request(sem_req):
    '''
    Processes request values and
    ensures all data valid

    Returns
    --------
    SeminarSlot if valid
    Raises ValueError if not valid
    '''
    # TODO: review future seminar period
    slots = SeminarSlot.objects.filter(
        start_datetime__gt=datetime.now(), id=sem_req[const.KEY_CHOICE]
    )
    if not slots:
        raise ValueError('No Seminar Available with that ID')

    # Check if student already added
    sem_slot = slots[0]
    if sem_slot.students.filter(email=sem_req[const.KEY_EMAIL]):
        raise ValueError('Student already registered')

    return sem_slot
