'''
Polyglossa payments models
'''
from django.db import models

from class_bookings import models as cb_models


class Order(models.Model):
    '''
    Tracks order and payments status

    Keeps data to be transformed
    '''
    class PaymentStatus(models.TextChoices):
        '''Payment Status Enum'''
        AWAITING = 'awaiting payment'
        COMPLETE = 'payment complete'
        FAILED = 'payment failed'

    class Processors(models.TextChoices):
        '''Enums for processor to perform further order actions'''
        SEM = 'SemSlotProcessor'
        IND = 'IndSlotProcessor'

    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(cb_models.Student, on_delete=models.PROTECT)
    payment_status = models.CharField(choices=PaymentStatus.choices)
    order_processor = models.TextField(choices=Processors.choices)
    order_serialised = models.CharField()
