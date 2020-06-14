'''
Handler for payment signals
'''
from django.shortcuts import get_object_or_404
from django.dispatch import receiver

from paypal.standard.ipn.signals import valid_ipn_received

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
        "Order=%r, ipn.payment_status=%r" % (
            ipn.invoice,
            ipn.payment_status.upper(),
        )
    )

    order = get_object_or_404(Order, id=ipn.invoice)
    if ipn.payment_status.upper() == 'COMPLETED':
        if order.amount == ipn.mc_gross:
            order.payment_status = Order.PaymentStatus.COMPLETED
            # TODO: add in handler actions
        else:
            print("Order amount didn't match: {}!={}".format(
                order.amount, ipn.mc_gross
            ))
    else:
        order.payment_status = Order.PaymentStatus.FAILED

    order.save()
