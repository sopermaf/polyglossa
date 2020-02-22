'''These are the request handlers for the class_bookings
section of the polyglossa website.
'''
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
    except KeyError as excp:
        print(f"POST Seminar parsing failed\nMissing param: '{excp}'\nParams: {request.POST}")
        return util.http_bad_request(
            msg="Missing booking param"
        )

    # Validation
    try:
        sem_slot = validate.validate_seminar_request(sem_req)
    except ValueError as excp:
        print(f"POST Seminar validation failed: {excp}\nParams: {request.POST}")
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


def get_activities(request, activity_type): #pylint: disable=unused-argument
    '''Return all the `bookable` activities
    for a given `activity_type`.
    '''
    activities = models.Activity.objects.filter(
        activity_type=activity_type,
        is_bookable=True,
    ).values()
    print(f"GET Request for Type: {activity_type}\n{activities}")

    return JsonResponse({'activities': list(activities)})


def get_future_seminar_slots(request, seminar_id): #pylint: disable=unused-argument
    '''Return all upcoming SeminarSlots for a given `seminar_id`'''
    slots = list(
        models.SeminarSlot.objects.filter(
            start_datetime__gt=datetime.now(),
            seminar__id=seminar_id,
        ).values()
    )

    return JsonResponse({'slots': slots})
