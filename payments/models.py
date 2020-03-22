'''
Polyglossa payments models
'''
from django.db import models
from django.utils import timezone

from . import processors
from class_bookings import models as cb_models


class Order(models.Model):
    '''
    Tracks order and payments status

    Keeps data to be transformed
    '''
    class PaymentStatus(models.TextChoices):
        '''Payment Status Enum'''
        AWAITING = 'Awaiting'
        COMPLETE = 'Complete'
        FAILED = 'Failed'

    class ProcessorEnums(models.TextChoices):
        '''Enums for processor to perform further order actions'''
        SEMINAR = 'SemSlotProcessor'
        INDIVIDUAL = 'IndSlotProcessor'

    customer = models.ForeignKey(cb_models.Student, on_delete=models.PROTECT)
    payment_status = models.CharField(
        choices=PaymentStatus.choices, max_length=20, default=PaymentStatus.AWAITING,
    )
    processor = models.CharField(choices=ProcessorEnums.choices, max_length=30)
    order_details = models.TextField(editable=False)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):    # pylint: disable=arguments-differ
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Order, self).save(*args, **kwargs)

    def success(self):
        '''Perform payment success operations

        Unserialise data and process.

        Returns
        ---
        None
        '''
        order_processor = getattr(processors, self.processor)()
        order_processor.complete(self.order_details)
        self.payment_status = self.PaymentStatus.COMPLETE
        self.save()

    def failure(self):
        '''Perform payment failure operations

        Returns
        ---
        None
        '''
        self.payment_status = self.PaymentStatus.FAILED
        self.save()
