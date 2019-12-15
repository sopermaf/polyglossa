'''These are the request handlers for the class_bookings
section of the polyglossa website.
'''
import json

from datetime import datetime as dt
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

import class_bookings.util as cb_utils
import class_bookings.models as models
import class_bookings.data_transform as transform
from class_bookings.validation import validate_booking_request

@csrf_exempt
def post_booking(request):
    '''Receive a lesson post request, perform validation, and store
    the request if valid.

    Returns a HTTP code to indicate success or failure of request
    '''
    lesson_request = {}
    for booking_key in cb_utils.BOOKING_POST_KEYS:
        try:
            lesson_request[booking_key] = request.POST[booking_key]
        except KeyError as excp:
            print(excp)
            return cb_utils.http_bad_request(str(excp))

    print(f"Data received: {lesson_request}")
    # validation stage
    try:
        validate_booking_request(lesson_request)
    except ValueError as validation_excp:
        print("Validation failed on request")
        print(validation_excp)
        return cb_utils.http_bad_request(str(validation_excp))


    student = models.Student.get_existing_or_create(
        lesson_request[cb_utils.REQUEST_KEY_NAME],
        lesson_request[cb_utils.REQUEST_KEY_EMAIL],
    )
    lesson = models.LessonType.objects.get(    # pylint: disable=no-member
        title=lesson_request[cb_utils.REQUEST_KEY_LESSON_CHOICE]
    )

    requested_booking = models.Booking(
        student=student,
        lessonType=lesson,
        lesson_datetime=dt.strptime(
            lesson_request[cb_utils.REQUEST_KEY_TIME],
            cb_utils.FORMAT_BOOKING_DATETIME
        ),
    )
    requested_booking.save()

    return cb_utils.http_resource_created()


def get_form(request):
    '''Loads the booking request
    page and sends the relevant limiting
    information on times, dates, and lessonTypes
    allowable
    '''
    # Load times
    # Load max/min and avail dates

    bookable_lessons_details = transform.get_bookable_lesson_details()

    context = {
        "booking_data": json.dumps({
            'avail_dates': [],
            'lesson_types': bookable_lessons_details,
            'time_slots': [],
        })
    }
    return render(request, "bookClass.html", context)
