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
        slots = util.create_seminar_slots(activity)
        self.slot = slots['future']

        self.order = Order.objects.create(
            customer=self.student,
            payment_status=Order.PaymentStatus.AWAITING,
            processor=Order.ProcessorEnums.SEMINAR,
            order_details=json.dumps({
                const.KEY_CHOICE: self.slot.id,
                const.KEY_NAME: self.student.name,
                const.KEY_EMAIL: self.student.email,
            }),
        )
