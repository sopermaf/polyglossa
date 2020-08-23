'''These are the request handlers for the class_bookings
section of the polyglossa website.
'''
import json
from datetime import datetime

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.middleware.csrf import get_token

from payments.models import Order
from payments.views import paypal_button

from . import parse, const, util
from . import models


def post_seminar_student(request):
    '''
    Receive a Seminar Request and create
    an `Order` which can then be completed
    upon payment.

    Redirects to the Paypal payments page.
    '''
    # Parsing
    try:
        sem_req = parse.parse_seminar_request(request)
    except KeyError as excp:
        print(f"POST Seminar parsing failed\nMissing param: '{excp}'\nParams: {request.POST}")
        return util.http_bad_request(
            msg="Missing booking param"
        )

    # create student
    student = models.Student.get_existing_or_create(
        name=sem_req[const.KEY_NAME],
        email=sem_req[const.KEY_EMAIL],
    )

    # Validate Slot Selection
    try:
        slot = models.SeminarSlot.validate_booking(sem_req[const.KEY_CHOICE], student)
        awaiting_orders = Order.objects.filter(
            customer__pk=student.pk, payment_status=Order.PaymentStatus.AWAITING
        )
        for order in awaiting_orders:
            order_details = json.loads(order.order_details)
            if order_details[str(const.KEY_CHOICE)] == str(slot.pk):
                raise ValidationError(f'Student {student} already has an upcoming order {order}')
    except ValidationError as excp:
        print(f"POST Seminar validation failed: {excp}\nParams: {request.POST}")
        return util.http_bad_request(
            msg='Bad Request'
        )

    order = Order(
        customer=student,
        processor=Order.ProcessorEnums.SEMINAR,
        order_details=json.dumps(sem_req),
        amount=slot.seminar.price,
    )
    order.save()

    return paypal_button(request, order, status=const.RESOURCE_CREATED_CODE)


def get_activities(request, activity_type): #pylint: disable=unused-argument
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


def get_future_seminar_slots(request, seminar_id): #pylint: disable=unused-argument
    '''Return all upcoming SeminarSlots for a given `seminar_id`'''
    slots = list(
        models.SeminarSlot.objects.filter(
            start_datetime__gt=datetime.now(),
            seminar__id=seminar_id,
        ).values()
    )

    return JsonResponse({'slots': slots})
