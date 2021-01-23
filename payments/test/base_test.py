'''
Base test class for polyglossa payments
'''
import json

from django.test import TestCase

from class_bookings.test import util
from class_bookings import models as cb_models
from class_bookings import const

from ..models import Order

class TestPayments(TestCase):
    '''
    Base Test class with setup procedure
    for testing polyglossa/orders
    '''
    def setUp(self):
        self.student = cb_models.Student.objects.create(
            name='bob', email='bob@test.com'
        )

        activity = util.create_activity(
            activity_type=cb_models.Activity.SEMINAR,
            bookable=True,
        )
        slots = util.create_seminar_slot_pair(activity)
        self.slot = slots['future']

        self.order_details = {
            const.KEY_CHOICE: self.slot.id,
            const.KEY_NAME: self.student.name,
            const.KEY_EMAIL: self.student.email,
        }
        self.order = Order.objects.create(
            customer=self.student,
            payment_status=Order.PaymentStatus.AWAITING,
            processor=Order.ProcessorEnums.SEMINAR,
            processor_data=json.dumps(self.order_details),
            amount=self.slot.seminar.price,
        )

    # helper functions

    def student_in_seminar(self):
        '''
        Check if student in seminar students

        Returns
        ---
        bool - (true if present, false if absent)
        '''
        return self.slot.students.filter(pk=self.student.pk)
