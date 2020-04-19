'''
Request handlers for Polyglossa payments
'''
import re

from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from paypal.standard.forms import PayPalEncryptedPaymentsForm

from polyglossa import settings

ENCRYPTED_BUTTON_REGEX = re.compile(r'(?<=name="encrypted" value=")([^"]+)', re.DOTALL)


def paypal_button(request, order, status):
    '''
    Send the encrypted button info for
    a given order
    '''
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_EMAIL,
        'amount': '10.00',
        'item_name': 'Order 1',
        'invoice': '101',
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('index')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('index')),
    }
    form = PayPalEncryptedPaymentsForm(initial=paypal_dict)
    button_address = ENCRYPTED_BUTTON_REGEX.search(form.render()).group()

    payment_data = {
        'button': {
            'address': button_address,
        },
        'order': {
            'email': order.customer.email,
            'name': order.customer.name,
            'amount': order.amount,
            'ref': paypal_dict['invoice'],
        },
    }
    return JsonResponse(payment_data, status=status)


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

    # parse student
    # get Awaiting Order
    # cancel awaiting Order

    return HttpResponse("cancelled")
