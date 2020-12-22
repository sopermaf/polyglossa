"""Test custom manage.py commands"""
# pylint: disable=missing-class-docstring,missing-function-docstring

from io import StringIO
import re

from django.core.management import call_command
from django.test import TestCase

from tasks.models import EmailTask


class TestCommandSendEmailTasks(TestCase):
    COMMAND = 'send_email_tasks'
    RE_SENT_EMAIL = re.compile(r'EmailTask\(id=.+\) sent', re.MULTILINE)

    def setUp(self):
        self.email_task = EmailTask.objects.create()

    def test_email_sent(self):
        # run command
        out = StringIO()
        call_command(self.COMMAND, stdout=out)
        self.email_task.refresh_from_db()

        # ensure email sent
        self.assertTrue(self.email_task.sent)
        if not self.RE_SENT_EMAIL.search(out.getvalue()):
            raise ValueError('Email not sent')

    def test_emails_not_resent(self):
        # setup
        self.email_task.sent = True
        self.email_task.save()

        # run command
        out = StringIO()
        call_command(self.COMMAND, stdout=out)

        # ensure email not resent
        if self.RE_SENT_EMAIL.search(out.getvalue()):
            raise ValueError('Email resent')
