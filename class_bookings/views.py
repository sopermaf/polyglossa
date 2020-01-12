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


# TODO: update with new Activity model
@csrf_exempt
def post_individual_booking(request):
    '''Receive a lesson post request, perform validation, and store
    the request if valid.

    Returns a HTTP code to indicate success or failure of request
    '''
    try:
        lesson_request = cb_utils.parse_post_booking(request)
    except (KeyError, ValueError) as excp:
        print(f"Booking Request Failed\n\n:{excp}")
        return cb_utils.http_bad_request(str(excp))

    student = models.Student.get_existing_or_create(
        lesson_request[cb_utils.REQUEST_KEY_NAME],
        lesson_request[cb_utils.REQUEST_KEY_EMAIL],
    )
    lesson = models.LessonType.objects.get(
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
    # TODO: load available slots based on form

    bookable_lessons_details = transform.get_bookable_lesson_details()

    context = {
        "booking_data": json.dumps({
            'avail_dates': [],
            'lesson_types': bookable_lessons_details,
            'time_slots': [],
        })
    }
    return render(request, "bookClass.html", context)
