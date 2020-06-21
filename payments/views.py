'''
Request handlers for Polyglossa payments
'''
import re

from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect

from paypal.standard.forms import PayPalEncryptedPaymentsForm

from payments.models import Order

from polyglossa import settings

ENCRYPTED_BUTTON_REGEX = re.compile(r'(?<=name="encrypted" value=")([^"]+)', re.DOTALL)
RE_FORM_URL = re.compile(r'(?<=action=")([^"]+)',)


def paypal_button(request, order, status, **kwargs):
    '''
    Send the encrypted button info for
    a given order
    '''
    # create paypal form
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_EMAIL,
        'amount': order.amount,
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

    # extract key parts for Vue form
    form_str = form.render()
    button_address = ENCRYPTED_BUTTON_REGEX.search(form_str).group()
    form_url = RE_FORM_URL.search(form_str).group()

    payment_overview = {
        'button': {
            'address': button_address,
            'url': form_url,
        },

        # custom_display order details
        'order': kwargs.copy(),
    }
    payment_overview['order']['email'] = order.customer.email
    payment_overview['order']['name'] = order.customer.name
    payment_overview['order']['amount'] = paypal_dict['amount']
    payment_overview['order']['currency'] = paypal_dict['currency_code']

    request.session['order_id'] = order.id

    return JsonResponse(payment_overview, status=status)


@csrf_exempt
def cancel_awaiting_order(request):
    '''
    Cancels an existing order based on session
    cookies.

    NOTE: Used on paypal and from payment page

    Parameters
    ---
    - request (post)

    Returns
    ---
    HttpResponse
    '''
    if 'order_id' not in request.session:
        print(f"No order found for {request}")
        return HttpResponse('Not Found', status=404)
    order_id = request.session['order_id']

    # only cancels awaiting orders
    order = get_object_or_404(
        Order,
        payment_status=Order.PaymentStatus.AWAITING,
        id=order_id,
    )

    order.payment_status = Order.PaymentStatus.CANCELLED
    order.save()
    print(f"Order {order} cancelled")

    return redirect('index')
