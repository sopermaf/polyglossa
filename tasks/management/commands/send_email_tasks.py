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

        unsent_email_tasks = EmailTask.unsent.all()
        if not unsent_email_tasks:
            self.stdout.write(self.style.SUCCESS('No EmailTasks to send'))
            return

        for email_task in unsent_email_tasks:
            email_task.send(connection)
            self.stdout.write('EmailTask(id=%r) sent' % email_task.id)
        self.stdout.write(self.style.SUCCESS('All EmailTasks sent'))
