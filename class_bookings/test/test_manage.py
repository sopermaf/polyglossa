"""Test custom manage.py commands"""
# pylint: disable=missing-class-docstring,missing-function-docstring

from datetime import timedelta
from io import StringIO
import re

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from class_bookings.models import SeminarSlot, Student, Activity


class SendSeminarRemindersTest(TestCase):
    COMMAND = 'send_seminar_reminders'
    RE_SENT_EMAIL = re.compile(r'Seminar\(.\) (?:day|hour) reminder sent', re.MULTILINE)

    def setUp(self):
        self.slot = SeminarSlot.objects.create(
            seminar=Activity.objects.create(price=10.2),
            start_datetime=timezone.now()
        )

        self.slot.students.add(
            Student.objects.create(email="test@example.com")
        )

    def test_day_email_sent(self):
        # set slot time to 23 hours in advance
        self.slot.start_datetime = timezone.now() + timedelta(hours=23)
        self.slot.save()

        # run command
        call_command(self.COMMAND)
        self.slot.refresh_from_db()

        # ensure only daily reminder sent
        self.assertTrue(self.slot.day_before_reminder_sent)

    def test_day_email_not_sent(self):
        # set slot time to 23 hours in advance
        self.slot.start_datetime = timezone.now() + timedelta(days=2)
        self.slot.hour_before_reminder_sent = True
        self.slot.save()

        # run command
        out = StringIO()
        call_command(self.COMMAND, stdout=out)
        self.slot.refresh_from_db()

        # ensure only daily reminder sent
        self.assertFalse(self.slot.day_before_reminder_sent)
        if self.RE_SENT_EMAIL.search(out.getvalue()):
            raise ValueError('Day reminder sent')

    def test_hour_email_sent(self):
        # set slot time to 23 hours in advance
        self.slot.start_datetime = timezone.now() + timedelta(minutes=59)
        self.slot.save()

        # run command
        call_command(self.COMMAND)
        self.slot.refresh_from_db()

        # ensure hour reminder email sent
        self.assertTrue(self.slot.hour_before_reminder_sent)

    def test_hour_email_not_sent(self):
        # setup test
        self.slot.start_datetime = timezone.now() + timedelta(hours=2)
        self.slot.day_before_reminder_sent = True
        self.slot.save()

        # run command
        out = StringIO()
        call_command(self.COMMAND, stdout=out)
        self.slot.refresh_from_db()

        # ensure hour reminder not sent
        self.assertFalse(self.slot.hour_before_reminder_sent)
        if self.RE_SENT_EMAIL.search(out.getvalue()):
            raise ValueError('hour reminder sent')

    def test_no_duplicate_reminders(self):
        self.slot.hour_before_reminder_sent = True
        self.slot.day_before_reminder_sent = True
        self.slot.save()

        out = StringIO()
        call_command(self.COMMAND, stdout=out)

        if self.RE_SENT_EMAIL.match(out.getvalue()):
            raise ValueError('Reminder email sent')
