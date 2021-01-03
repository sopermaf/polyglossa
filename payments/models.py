'''
Polyglossa payments models
'''
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
    processor = models.CharField(choices=ProcessorEnums.choices, max_length=30, editable=False)
    order_details = models.TextField(editable=False)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)


    def __str__(self):
        fields = [
            f'{field}:{val}'
            for field, val in self.__dict__.items()
            if not field.startswith('_')
        ]
        return ", ".join(fields)

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)

        if self.amount <= 0:
            raise ValidationError(
                f'<order.amount> must be a positive value. Found <{self.amount}>'
            )

    def save(self, *args, **kwargs):    # pylint: disable=signature-differs
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super().save(*args, **kwargs)

    def success(self):
        '''
        Perform payment success operations

        Unserialise order data and process based
        on the `processor` specified to complete
        the order.

        Returns
        ---
        None
        '''
        ProcessorClass = getattr(processors, self.processor) #pylint: disable=invalid-name

        order_processor = ProcessorClass(self.order_details)
        order_processor.complete()
        self.payment_status = self.PaymentStatus.COMPLETED
        self.save()

        # create an EmailTask for sending
        html_msg = render_to_string('tasks/order.html', {'order': self})

        EmailTask.objects.create(
            to_email=self.customer.email,
            subject='Order Confirmed',
            msg=html_msg,
        )


    def failure(self):
        '''
        Perform payment failure operations

        Returns
        ---
        None
        '''
        self.payment_status = self.PaymentStatus.FAILED
        self.save()
