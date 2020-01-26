'''These are the request handlers for the class_bookings
section of the polyglossa website.
'''
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt
from django.db.models import ObjectDoesNotExist

from . import parse, const, util
from .models import Student, SeminarSlot

@csrf_exempt
def seminar_booking(request):
    '''
    Process a request from the the form
    and add a student to the selected student
    '''
    # Get Relevant Info from Request
    try:
        sem_req = parse.parse_seminar_request(request)
    except KeyError as exc:
        return util.http_bad_request(
            msg="Missing booking param"
        )
    
    # NOTE: review future seminar period
    slots = SeminarSlot.objects.filter(
        start_datetime__gt=datetime.now(), id=sem_req[const.KEY_CHOICE]
    )
    if not slots:
        return util.http_bad_request('No Seminar Available with that ID')
    
    sem_slot = slots[0]
    student = Student.get_existing_or_create(
        name=sem_req[const.KEY_STUDENT_NAME],
        email=sem_req[const.KEY_EMAIL],
    )
    sem_slot.students.add(student)
    sem_slot.save()

    return util.http_resource_created()
