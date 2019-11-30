'''These are the request handlers for the class_bookings
section of the polyglossa website.
'''
from datetime import datetime as dt
from django.http import HttpResponse
import class_bookings.util as cb_utils
from class_bookings.models import LessonType, Student, Booking
from class_bookings.validation import validate_booking_request

# Create your views here.
def post_booking(request):
    '''Receive a lesson post request,
    perform validation, and store
    the request if valid.

    Returns a HTTP code to indicate
    success or failure of request
    '''
    lesson_request = {}
    for booking_key in cb_utils.BOOKING_POST_KEYS:
        try:
            lesson_request[booking_key] = request.POST[booking_key]
        except KeyError:
            error_response = HttpResponse()
            error_response.status_code = cb_utils.BAD_REQUEST_CODE
            error_response.content = f"Missing {booking_key} to reserve lesson"
            return error_response

    # validation stage
    try:
        validate_booking_request(lesson_request)
    except ValueError:
        print(f"Lesson Not Created: {lesson_request}")
        error_response = HttpResponse('Bad request')
        error_response.status_code = cb_utils.BAD_REQUEST_CODE
        return error_response

    #TODO: remove this logic from main
    student = Student.get_student_safe(
        lesson_request[cb_utils.REQUEST_KEY_EMAIL]
    )
    if student is None:
        student = Student(
            name=lesson_request[cb_utils.REQUEST_KEY_NAME],
            email=lesson_request[cb_utils.REQUEST_KEY_EMAIL],
        )
        student.save()

    # TODO: add tests and exception handling for this section
    lesson = LessonType.objects.get(    # pylint: disable=no-member
        title=lesson_request[cb_utils.REQUEST_KEY_LESSON_CHOICE]
    )

    requested_booking = Booking(
        student=student,
        lessonType=lesson,
        lesson_datetime=dt.strptime(
            lesson_request[cb_utils.REQUEST_KEY_TIME],
            cb_utils.FORMAT_BOOKING_DATETIME
        ),
    )
    requested_booking.save()

    # TODO: add logging
    print(f"Lesson Created: {requested_booking}")

    success_response = HttpResponse('Student and Lesson created')
    success_response.status_code = cb_utils.RESOURCE_CREATED_CODE
    return success_response
