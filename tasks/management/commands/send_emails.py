# pylint: disable=missing-class-docstring,import-error
from django.core.management.base import BaseCommand
from tasks.models import EmailTask


class Command(BaseCommand):
    help = 'Send all unsent email tasks'

    def handle(self, *args, **options):
        for email_task in EmailTask.unsent.all():
            email_task.send()
            self.stdout.write(
                self.style.SUCCESS('EmailTask(id=%r) sent' % email_task.id)
            )
        self.stdout.write(self.style.SUCCESS('All emails sent'))
