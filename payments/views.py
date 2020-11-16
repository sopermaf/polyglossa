'''
Request handlers for Polyglossa payments
'''
import re
import json
from django.http.response import Http404

from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render

from paypal.standard.forms import PayPalEncryptedPaymentsForm

from payments.models import Order

from polyglossa import settings

RE_ENCRYPTED_BUTTON = re.compile(r'(?<=name="encrypted" value=")([^"]+)', re.DOTALL)
RE_FORM_URL = re.compile(r'(?<=action=")([^"]+)',)


def order_page(request):
    '''
    Send the encrypted button info for
    a given order
    '''
    # get the created order
    if 'order_id' not in request.session:
        print(f"No order found for {request}")
        raise Http404('Order Not Found')
    order = get_object_or_404(
        Order,
        payment_status=Order.PaymentStatus.AWAITING,
        id=request.session['order_id'],
    )

    # create paypal form
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_EMAIL,
        'amount': '{:.2f}'.format(order.amount),
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

    payment_overview = {
        'order': [
            _order_item('name', order.customer.name),
            _order_item('email', order.customer.email),
            _order_item('amount', paypal_dict['amount']),
            _order_item('currency', paypal_dict['currency_code']),
        ]
    }

    # extract key parts for Vue form
    if order.amount > 0:
        form_str = form.render()
        encrypted_inputs = RE_ENCRYPTED_BUTTON.search(form_str).group()
        form_url = RE_FORM_URL.search(form_str).group()

        payment_overview['button'] = {
            'encrypted_inputs': encrypted_inputs,
            'url': form_url,
        }
    else:
        # no payment required
        payment_overview['button'] = None
        order.success()

    # render payments page
    context = {'data': json.dumps(payment_overview)}
    return render(request, 'payment.html', context)


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
        raise Http404('No existing order found to cancel')
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

    return HttpResponse('Order succesfully cancelled')


def _order_item(title, value):
    return {'title': title, 'value': value}
