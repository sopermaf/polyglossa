'''These are the request handlers for the class_bookings
section of the polyglossa website.
'''
import json
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from . import validate, parse, const, util
from . import models


@csrf_exempt
def post_seminar_student(request):
    '''
    Process a request from the the form
    and add a student to the selected student
    '''
    # Parsing
    try:
        sem_req = parse.parse_seminar_request(request)
    except KeyError:
        return util.http_bad_request(
            msg="Missing booking param"
        )

    # Validation
    try:
        sem_slot = validate.validate_seminar_request(sem_req)
    except ValueError:
        return util.http_bad_request(
            msg='Bad Request'
        )

    # Add student to seminar
    student = models.Student.get_existing_or_create(
        name=sem_req[const.KEY_NAME],
        email=sem_req[const.KEY_EMAIL],
    )
    sem_slot.students.add(student)
    sem_slot.save()

    return util.http_resource_created()


def get_seminar_form(request):
    '''
    Returns the seminar form page and a list
    of seminar activities passed as context
    '''
    seminars = list(
        models.Activity.objects.filter(
            is_bookable=True, activity_type=models.Activity.SEMINAR,
        ).values('title', 'id', 'price')
    )

    context = {
        "slot_info": json.dumps({
            'seminars': seminars,
        })
    }
    return render(request, "bookClass.html", context)


def get_future_seminar_slots(request, seminar_id): #pylint: disable=unused-argument
    '''Return all upcoming SeminarSlots for a given `seminar_id`'''
    slots = list(
        models.SeminarSlot.objects.filter(
            start_datetime__gt=datetime.now(),
            seminar__id=seminar_id,
        ).values()
    )

    return JsonResponse({'slots': slots})
