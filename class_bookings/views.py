'''These are the request handlers for the class_bookings
section of the polyglossa website.
'''
from django.views.decorators.csrf import csrf_exempt

from . import validate, parse, const, util
from .models import Student


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
    student = Student.get_existing_or_create(
        name=sem_req[const.KEY_NAME],
        email=sem_req[const.KEY_EMAIL],
    )
    sem_slot.students.add(student)
    sem_slot.save()

    return util.http_resource_created()
