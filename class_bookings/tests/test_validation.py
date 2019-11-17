from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime
import class_bookings.util as cb_utils
from class_bookings.models import Lesson, Student

class TestViews(TestCase):
    def setUp(self):       
        self.datetime_str = datetime.now().strftime(cb_utils.FORMAT_LESSON_DATETIME)
        self.name = 'ferdia'
        self.email = 'ferdia@example.com'

        self.student = Student(name=self.name, email=self.email)
        #self.lesson = Lesson(student=self.student, lesson_datetime=self.)

    def test_less(self):
        """ test lesson request creation """
        pass
        
