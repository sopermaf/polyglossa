"""
Send all unsent email tasks and mark them
as sent
"""
# pylint: disable=missing-class-docstring,import-error
from django.core.management.base import BaseCommand
from django.core.mail import get_connection

from class_bookings.models import SeminarSlot


class Command(BaseCommand):
    help = 'Send all unsent email tasks'

    def handle(self, *args, **options):
        conn = get_connection()

        hour_seminars = SeminarSlot.hour_reminder_unsent.all()
        self.send(hour_seminars, conn, 'hour')

        day_seminars = SeminarSlot.day_reminder_unsent.all()
        self.send(day_seminars, conn, 'day')


    def send(self, seminars, conn, reminder_type) -> None:
        """Send the seminar reminder"""
        if not seminars:
            self.stdout.write(
                self.style.SUCCESS('No current Seminar %s reminders to send' % reminder_type)
            )
            return

        for seminar in seminars:
            seminar.send_reminder(conn, reminder_type)
            self.stdout.write(
                'Seminar(id={}) {} reminder sent'.format(
                    seminar.id,
                    reminder_type,
                )
            )
        self.stdout.write(self.style.SUCCESS('Sent all %s reminders for Seminars' % reminder_type))
