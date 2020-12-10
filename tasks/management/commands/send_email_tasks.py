"""
Send all unsent email tasks and mark them
as sent
"""
# pylint: disable=missing-class-docstring,import-error
from django.core.management.base import BaseCommand
from django.core.mail import get_connection

from tasks.models import EmailTask


class Command(BaseCommand):
    help = 'Send all unsent email tasks'

    def handle(self, *args, **options):
        connection = get_connection(fail_silently=False)

        for email_task in EmailTask.unsent.all():
            email_task.send(connection)
            self.stdout.write(
                self.style.SUCCESS('EmailTask(id=%r) sent' % email_task.id)
            )
        self.stdout.write(self.style.SUCCESS('All emails sent'))
