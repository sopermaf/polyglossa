from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime
import class_bookings.util as cb
from class_bookings.models import Lesson, Student

class TestViews(TestCase):
    def setUp(self):       
        self.datetime_str = datetime.now().strftime(cb.FORMAT_TIME)
        self.name = 'ferdia'
        self.email = 'ferdia@example.com'
        self.student = Student(name=self.name, email=self.email)


    def test_less(self):
        """ test lesson request creation """
        pass
        
