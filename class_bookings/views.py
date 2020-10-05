'''These are the request handlers for the class_bookings
section of the polyglossa website.
'''
# pylint: disable=unused-argument
import json
from collections import defaultdict
from datetime import datetime, timedelta, date

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, get_object_or_404

from payments.models import Order
from payments.views import paypal_button
from . import parse, const, util, models
from . import errors as err


# CONSTANTS

UPCOMING_TIME_DELTA = timedelta(days=3)


# VIEWS

def seminar_video_page(request, slot_id: str):
    """Render the video page for the given slot"""
    slot = get_object_or_404(models.SeminarSlot, id=slot_id)

    context = {'video_id': slot.video_id}
    return render(request, 'class_bookings/video.html', context)


def seminar_signup(request):
    '''
    Attempt to create an Order for a student
    for the specified seminar.

    POST requests only

    Returns
    -------
    JSONResponse
        - order details
        - paypal secure button code
    HttpResponse
        if error occurs, with error message
    '''
    # parse request
    try:
        sem_req = parse.parse_seminar_request(request)
    except KeyError as excp:
        print(f"POST Seminar parsing failed\nMissing param: '{excp}'\nParams: {request.POST}")
        return util.http_bad_request(msg="Booking failed. Missing required data.")

    student, _ = models.Student.objects.get_or_create(
        email=sem_req[const.KEY_EMAIL],
        defaults={'name': sem_req[const.KEY_NAME]},
    )

    # validate request
    try:
        # validate slot and student
        slot = models.SeminarSlot.validate_signup(sem_req[const.KEY_CHOICE], student)

        # ensure no upcoming order
        awaiting_orders = Order.objects.filter(
            customer__pk=student.pk, payment_status=Order.PaymentStatus.AWAITING
        )
        for order in awaiting_orders:
            order_details = json.loads(order.order_details)
            if order_details[str(const.KEY_CHOICE)] == str(slot.pk):
                raise err.UnpaidOrderError(
                    f'Booking failed. {student} has existing {order} for {slot}'
                )
    except err.StudentAlreadyPresentError as excp:
        print(f'Booking failure\n\t{request.POST}\n\t{excp}')
        return util.http_bad_request('Student already signed up for this seminar')
    except err.SlotNotFoundError as excp:
        print(f'Booking failure\n\t{request.POST}\n\t{excp}')
        return util.http_bad_request('No matching slot found')
    except err.UnpaidOrderError as excp:
        print(f'Booking failure\n\t{request.POST}\n\t{excp}')
        return util.http_bad_request('Unpaid order found. Please contact support')

    order = Order(
        customer=student,
        processor=Order.ProcessorEnums.SEMINAR,
        order_details=json.dumps(sem_req),
        amount=slot.seminar.price,
    )
    order.save()

    return paypal_button(request, order, status=const.RESOURCE_CREATED_CODE)


def get_activities(request, activity_type):
    '''Return all the `bookable` activities
    for a given `activity_type`.
    '''
    token = get_token(request)
    activities = models.Activity.objects.filter(
        activity_type=activity_type,
        is_bookable=True,
    ).order_by('order_shown', 'title').values()
    print(f"GET Request for Type: {activity_type}\n{activities}")

    return JsonResponse({
        'activities': list(activities),
        'token': token,
    })


def get_future_seminar_slots(request, seminar_id):
    '''Return all upcoming SeminarSlots for a given `seminar_id`'''
    slots = list(
        models.SeminarSlot.objects.filter(
            start_datetime__gt=datetime.now(),
            seminar__id=seminar_id,
        ).order_by('start_datetime').values()
    )

    return JsonResponse({'slots': slots})


def get_upcoming_seminars(request):
    """
    Returns seminars with upcoming slots between now and future
    point that is `UPCOMING_TIME_DELTA` into the future

    Returns
    -------
    JSONResponse
        list of dicts with seminars grouped by date
    """
    now = datetime.now()

    upcoming = models.SeminarSlot.objects.filter(
        start_datetime__gt=now,
        start_datetime__lte=(now + UPCOMING_TIME_DELTA),
    )

    # creates a set of each day
    seminars_per_days = defaultdict(set)
    for slot in upcoming:
        seminars_per_days[slot.start_datetime.date()].add(slot.seminar.title)

    # format as a list
    formatted_days_and_seminars = [
        {
            'date': date,
            'seminars': sorted(seminars),
        }
        for date, seminars in seminars_per_days.items()
    ]

    formatted_days_and_seminars.sort(key=lambda day: day['date'])

    return JsonResponse(formatted_days_and_seminars, safe=False, encoder=_HomePageDateSerializer)


class _HomePageDateSerializer(DjangoJSONEncoder):
    """
    Serialisation of dates and datetime added
    """
    def default(self, obj): # pylint: disable=arguments-differ
        if isinstance(obj, (datetime, date)):
            return obj.strftime('%b %d')
        return super().default(obj)
