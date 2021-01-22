"""
Handler for payment signals
"""
from pprint import pprint

from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received

from .models import Order


@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs): # pylint: disable=unused-argument
    '''
    Handles the valid paypal IPN signal
    and sets the order status to the IPN update

    Returns
    ---
    None
        Order Status modified
    '''
    ipn = sender
    print(
        "IPN Received. Order=%r, ipn.payment_status=%r" % (
            ipn.invoice,
            ipn.payment_status.upper(),
        )
    )
    pprint(vars(ipn), indent=4)

    order = get_object_or_404(Order, id=ipn.invoice)
    if ipn.payment_status.upper() == 'COMPLETED' and order.amount == ipn.mc_gross:
        order.success()
    else:
        if order.amount != ipn.mc_gross:
            print("Order amount didn't match: {}!={}".format(
                order.amount, ipn.mc_gross
            ))

        order.failure()


@receiver(invalid_ipn_received)
def invalid_paypal_notification(sender, **kwargs):  # pylint: disable=unused-argument
    """Log failed signals received by Paypal"""
    ipn = sender
    print("Invalid paypal IPN received shown below")
    pprint(vars(ipn), indent=4)
