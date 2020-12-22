'''Deserialise objects stored in orders
and perform any needed actions
'''
import json

from class_bookings import models as cb_models
from class_bookings import const as cb_const

class OrderProcessor:   # pylint: disable=too-few-public-methods
    '''
    Base template class for
    completing an Order
    '''
    def __init__(self, order_details):
        self.order_details = json.loads(order_details)

    def complete(self):
        '''
        Perform actions to complete the order

        Returns
        ---
        None
        '''
        raise NotImplementedError


class SemSlotProcessor(OrderProcessor): # pylint: disable=too-few-public-methods
    '''Order Processor for Seminar Slots'''

    def complete(self):
        '''
        Add a student to the seminar slot

        Returns
        ---
        None
        '''
        student, _ = cb_models.Student.objects.get_or_create(
            email=self.order_details[cb_const.KEY_EMAIL],
            defaults={'name': self.order_details[cb_const.KEY_NAME]},
        )

        slot = cb_models.SeminarSlot.objects.get(
            id=self.order_details['slot_id']
        )

        slot.students.add(student)
        slot.save()

        # send email
