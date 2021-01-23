'''These are the request handlers for the class_bookings
section of the polyglossa website.
'''
# pylint: disable=unused-argument
import json
from collections import defaultdict
import datetime

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.http.response import Http404, HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from payments.models import Order
from . import parse, const, util, models
from . import errors as err


# CONSTANTS

UPCOMING_TIME_DELTA = datetime.timedelta(days=3)
AVAIL_VIDEO_LIMIT = datetime.timedelta(days=1)

# VIEWS

def seminar_video_page(request, slot_id):
    """Render the video page for the given slot"""
    slot = get_object_or_404(models.SeminarSlot, external_id=slot_id)

    # validate time period
    now = timezone.now()
    limit_time = slot.start_datetime + AVAIL_VIDEO_LIMIT
    if now < slot.start_datetime or now >= limit_time:
        raise Http404('Seminar not currently available')

    # render video page
    context = {
        'data': json.dumps({
            "video_id": slot.video_id,
            "title": slot.seminar.title,
        })
    }
    return render(request, 'video.html', context)


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

        # cancel upcoming order if not paid and trying to reorder
        awaiting_orders = Order.objects.filter(
            customer__pk=student.pk,
            payment_status=Order.PaymentStatus.AWAITING
        )
        for order in awaiting_orders:
            processor_data = json.loads(order.processor_data)
            if processor_data[str(const.KEY_CHOICE)] == str(slot.pk):
                order.payment_status = Order.PaymentStatus.CANCELLED
                order.save()
    except err.StudentAlreadyPresentError as excp:
        print(f'Booking failure\n\t{request.POST}\n\t{excp}')
        return util.http_bad_request('Student already signed up for this seminar')
    except err.SlotNotFoundError as excp:
        print(f'Booking failure\n\t{request.POST}\n\t{excp}')
        return util.http_bad_request('No matching slot found')

    order = Order.objects.create(
        customer=student,
        processor=Order.ProcessorEnums.SEMINAR,
        processor_data=json.dumps(sem_req),
        purchased_detail='{}, available for 24 hours from {} UTC'.format(
            slot.seminar.title,
            slot.start_datetime.strftime('%d-%b-%Y, %H:%M'),
        ),
        amount=slot.seminar.price,
    )
    request.session['order_id'] = order.id

    return HttpResponse('Order successfully created', status=201)


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
            start_datetime__gt=timezone.now(),
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
    now = timezone.now()

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
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.strftime('%b %d')
        return super().default(obj)
