'''These are the request handlers for the class_bookings
section of the polyglossa website.
'''
from datetime import datetime as dt
import class_bookings.util as cb_utils
from class_bookings.models import LessonType, Student, Booking
from class_bookings.validation import validate_booking_request

# Create your views here.
def post_booking(request):
    '''Receive a lesson post request, perform validation, and store
    the request if valid.

    Returns a HTTP code to indicate success or failure of request
    '''
    lesson_request = {}
    for booking_key in cb_utils.BOOKING_POST_KEYS:
        try:
            lesson_request[booking_key] = request.POST[booking_key]
        except KeyError:
            return cb_utils.http_bad_request(f"Missing {booking_key} to reserve lesson")

    # validation stage
    try:
        validate_booking_request(lesson_request)
    except ValueError:
        return cb_utils.http_bad_request()


    student = Student.get_existing_or_create(
        lesson_request[cb_utils.REQUEST_KEY_NAME],
        lesson_request[cb_utils.REQUEST_KEY_EMAIL],
    )
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

    return cb_utils.http_resource_created()
