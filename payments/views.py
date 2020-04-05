'''
Request handlers for Polyglossa payments
'''
import re

from django.urls import reverse
from django.shortcuts import render
from django.http import JsonResponse

from paypal.standard.forms import PayPalEncryptedPaymentsForm

from polyglossa import settings

ENCRYPTED_BUTTON_REGEX = re.compile(r'(?<=name="encrypted" value=")([^"]+)', re.DOTALL) 

# Create your views here.
def paypal_form(request):
    '''Load the paypal form with payment info'''
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_EMAIL,
        'amount': '1.00',
        'item_name': 'Order 1',
        'invoice': '101010101',
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('index')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('index')),
    }

    # Create the instance.
    form = PayPalEncryptedPaymentsForm(initial=paypal_dict)
    print(form.render())

    context = {"form": form, 'payment_details': paypal_dict, 'test': form.render()}
    return render(request, "payment.html", context)


def paypal_button(request):
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_EMAIL,
        'amount': '1.00',
        'item_name': 'Order 1',
        'invoice': '101010101',
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('index')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('index')),
    }

    # Create the instance.
    form = PayPalEncryptedPaymentsForm(initial=paypal_dict)

    button = ENCRYPTED_BUTTON_REGEX.search(form.render()).group()

    data = {'button': button}
    return JsonResponse(data)
