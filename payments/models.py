'''
Polyglossa payments models
'''
import uuid

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string

from class_bookings import models as cb_models
from tasks.models import EmailTask
from . import processors


class Order(models.Model):
    '''
    Tracks order and payments status

    Keeps data to be transformed
    '''
    class PaymentStatus(models.TextChoices):
        '''Payment Status Enum'''
        AWAITING = 'Awaiting'
        COMPLETED = 'Completed'
        FAILED = 'Failed'
        CANCELLED = 'Cancelled'
        DENIED = 'Denied'
        REFUNDED = 'Refunded'

    class ProcessorEnums(models.TextChoices):
        '''Enums for processor to perform further order actions'''
        SEMINAR = 'SemSlotProcessor'
        INDIVIDUAL = 'IndSlotProcessor'

    customer = models.ForeignKey(cb_models.Student, on_delete=models.PROTECT, editable=False)
    payment_status = models.CharField(
        choices=PaymentStatus.choices, max_length=20, default=PaymentStatus.AWAITING,
    )
    amount = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    processor = models.CharField(choices=ProcessorEnums.choices, max_length=30, editable=False)
    processor_data = models.TextField(editable=False)
    purchased_detail = models.TextField(editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    payment_received = models.DateTimeField(editable=False, null=True)


    def __str__(self):
        return "Order(id={})".format(self.id)

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)

        if self.amount < 0:
            raise ValidationError(
                f'Order.amount must be a positive value. Given <{self.amount}>'
            )

    def success(self) -> None:
        """Perform payment success operations

        Unserialise order data and process based
        on the `processor` specified to complete
        the order.
        """
        ProcessorClass = getattr(processors, self.processor) #pylint: disable=invalid-name
        processor = ProcessorClass(self.processor_data)
        processor.complete()

        self.payment_status = self.PaymentStatus.COMPLETED
        self.payment_received = timezone.now()
        self.save()

        html_msg = render_to_string('payments/order.html', {'order': self})

        EmailTask.objects.create(
            to_email=self.customer.email,
            subject='Order Confirmed',
            msg=html_msg,
        )


    def failure(self) -> None:
        """Perform payment failure operations"""
        self.payment_status = self.PaymentStatus.FAILED
        self.save()
