'''These are the request handlers for the class_bookings
section of the polyglossa website.
'''
import json
from datetime import datetime

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
    '''Get the form and available slots'''
    slots = []
    for slot in models.SeminarSlot.objects.filter(start_datetime__gt=datetime.now()):
        activity = models.Activity.objects.get(id=slot.seminar_id)
        slot_info = {
            'price': activity.price,
            'title': activity.title,
            'id': slot.id,
            'datetime_pretty': slot.start_datetime.strftime('%d-%b %a%l:%M%p'),
            'datetime_iso': slot.start_datetime.strftime('%Y-%m-%dT%H:%M'),
            'duration': slot.duration_in_mins,
        }
        slots.append(slot_info)

    print(slots)

    context = {
        "slot_info": json.dumps({
            "seminar_slots": slots
        })
    }

    return render(request, "bookClass.html", context)
