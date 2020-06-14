'''
Request handlers for Polyglossa payments
'''
import re

from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from paypal.standard.forms import PayPalEncryptedPaymentsForm

from class_bookings.models import Student
from payments.models import Order

from polyglossa import settings

ENCRYPTED_BUTTON_REGEX = re.compile(r'(?<=name="encrypted" value=")([^"]+)', re.DOTALL)


def paypal_button(request, order, status, **kwargs):
    '''
    Send the encrypted button info for
    a given order
    '''
    host = request.get_host()

    # custom_display order details
    payment_overview = {
        'button': {},
        'order': kwargs.copy(),
    }

    # mandatory display details
    payment_overview['order']['email'] = order.customer.email
    payment_overview['order']['name'] = order.customer.name
    payment_overview['order']['amount'] = order.amount


    # used to generate the public key
    # TODO: add the rest of this info to paypal button
    paypal_dict = {
        'business': settings.PAYPAL_EMAIL,
        'amount': payment_overview['order']['amount'],
        'item_name': 'Order %s' % order.id,
        'invoice': str(order.id),   # NOTE: used to updated order
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('index')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('cancel-awaiting')),
    }
    form = PayPalEncryptedPaymentsForm(initial=paypal_dict)

    button_address = ENCRYPTED_BUTTON_REGEX.search(form.render()).group()
    payment_overview['button']['address'] = button_address

    return JsonResponse(payment_overview, status=status)


@csrf_exempt
def cancel_awaiting_order(request):
    '''
    Process a POST cancelation request for a student
    before a paypal IPN signal is used.

    Parameters
    ---
    - request (post)

    Returns
    ---
    HttpResponse
    '''
    if request.method != "POST":
        return HttpResponse("POST requests only", status=400)

    try:
        student_data = {key: request.POST[key] for key in ['name', 'email']}
    except KeyError:
        return HttpResponse("Missing parameters", status=400)

    student = get_object_or_404(
        Student,
        name=student_data['name'],
        email=student_data['email'],
    )

    order = get_object_or_404(
        Order,
        payment_status=Order.PaymentStatus.AWAITING,
        customer=student,
    )

    order.payment_status = Order.PaymentStatus.FAILED
    order.save()

    return HttpResponse("cancelled")    # TODO: return to home page
