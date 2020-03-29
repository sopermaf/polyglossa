'''
Request handlers for Polyglossa payments
'''
from django.urls import reverse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from paypal.standard.forms import PayPalEncryptedPaymentsForm

from polyglossa import settings

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
                                           reverse('payment-complete')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment-cancelled')),
    }

    # Create the instance.
    form = PayPalEncryptedPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment.html", context)


@csrf_exempt
def payment_complete(request):  # pylint: disable=unused-argument
    '''Successful Return'''
    return HttpResponse('Payment Complete')

@csrf_exempt
def payment_cancelled(request): # pylint: disable=unused-argument
    '''Successful Return'''
    return HttpResponse('Payment Cancelled')
