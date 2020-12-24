'''This is design of the tables that are used
in the database to manage the class_bookings
module
'''
# pylint: disable=unused-variable,too-few-public-methods,missing-class-docstring

from datetime import timedelta
from typing import Any
import uuid
import datetime

from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.db import models
from django.urls.base import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.template.loader import render_to_string

from .parse import parse_dt_as_str
from . import errors

# NOTE: calling the save() method directly avoids clean() validation


class Student(models.Model):
    '''
    Represents a student taking lessons on the site.
    '''
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name}, {self.email}"


class Activity(models.Model):
    '''
    Activity represents the types of bookable
    activities for students to reserve, and
    contains all information including pricing and
    descriptions, but not time information.
    '''
    INDIVIDUAL = "IND"
    SEMINAR = "SEM"
    ACTIVITY_TYPES = [
        (INDIVIDUAL, "one-on-one lesson"),
        (SEMINAR, "group seminar"),
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    is_bookable = models.BooleanField(default=False)
    activity_type = models.CharField(
        max_length=3,
        choices=ACTIVITY_TYPES,
        default=SEMINAR,
    )

    # related to showing on homepage
    order_shown = models.PositiveSmallIntegerField(default=100)
    is_highlighted = models.BooleanField(default=False)

    def __str__(self):
        booking_status = "Bookable" if self.is_bookable else "Not Bookable"
        return f"{self.title} (${self.price:.2f})"

    def __repr__(self):
        return f"<{self.activity_type}: {self.title},{self.price},{self.is_bookable}>"


class DayBeforeReminderManager(models.Manager):
    # pylint: disable=missing-function-docstring
    def get_queryset(self):
        limit = timezone.now() + timedelta(days=1)
        return super().get_queryset().filter(
            day_before_reminder_sent=False,
            start_datetime__lt=limit
        )


class HourBeforeReminderManager(models.Manager):
    # pylint: disable=missing-function-docstring
    def get_queryset(self):
        limit = timezone.now() + timedelta(hours=1)
        return super().get_queryset().filter(
            hour_before_reminder_sent=False,
            start_datetime__lt=limit
        )


class BaseSlot(models.Model):
    '''
    Defines a bookable slot for students to
    join
    '''
    class ReminderTypes(models.TextChoices):
        HOUR = 'hour'
        DAY = 'day'

    start_datetime = models.DateTimeField('The lesson date and time', )
    duration_in_mins = models.PositiveSmallIntegerField(default=60)
    day_before_reminder_sent = models.BooleanField(default=False)
    hour_before_reminder_sent = models.BooleanField(default=False)

    objects = models.Manager()
    hour_reminder_unsent = HourBeforeReminderManager()
    day_reminder_unsent = DayBeforeReminderManager()

    @property
    def end_datetime(self):
        ''' Returns the end datetime of a lesson '''
        return self.start_datetime + datetime.timedelta(minutes=self.duration_in_mins)

    def __str__(self):
        return f"{parse_dt_as_str(self.start_datetime)} ({self.duration_in_mins} mins)"

    def clean(self, *args, **kwargs): # pylint: disable=arguments-differ
        super().clean(*args, **kwargs)

        if self.start_datetime < timezone.now():
            raise ValidationError('Slot start must be in the future')

        upcoming_slots = BaseSlot.objects \
                                .filter(start_datetime__gt=timezone.now()) \
                                .exclude(id=self.id)
        for slot in upcoming_slots:
            if (max(slot.start_datetime, self.start_datetime)
                    < min(slot.end_datetime, self.end_datetime)):
                raise ValidationError(
                    f'Overlap with existing slot: {slot.start_datetime} - {slot.end_datetime}'
                )

    def safe_save(self):
        '''Ensures that the clean function is called before save'''
        self.clean()
        self.save()

    def send_reminder(self, connection: Any, reminder_type: str) -> None:   # pylint:disable=unused-argument
        """Base method for sending reminders about slot"""
        reminder_type = self.ReminderTypes(reminder_type.lower())
        if reminder_type == self.ReminderTypes.HOUR:
            self.hour_before_reminder_sent = True
        elif reminder_type == self.ReminderTypes.DAY:
            self.day_before_reminder_sent = True
        else:
            raise NotImplementedError('No Boolean value for ReminderType %s' % reminder_type)

        self.save()


class SeminarSlot(BaseSlot):
    """
    A seminar datetime slot bookable by a student

    Activity chosen upon slot creation by admin.
    """
    external_id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4
    )
    seminar = models.ForeignKey(
        Activity,
        limit_choices_to={
            "activity_type": Activity.SEMINAR,
            "is_bookable": True,
        },
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )
    students = models.ManyToManyField(Student, blank=True)
    video_id = models.CharField(max_length=20)

    def get_absolute_url(self):
        """Video page for seminar"""
        return reverse(
            'video-view',
            kwargs={'slot_id': self.external_id},
        )

    @classmethod
    def validate_signup(cls, slot_id, student):
        '''
        Ensure a student can sign up for the given
        SeminarSlot specified by its id.

        Parameters
        ----------
        - slot_id   : int (id of SeminarSlot to join)
        - student   : Student (student who wants to join)

        Raises
        ------
        - SlotNotFoundError          : no upcoming slot found
        - StudentAlreadyPresentError : student already in slot

        Returns
        -------
        SeminarSlot
            if signup valid
        '''
        # ensure future slot
        slots = cls.objects.filter(
            start_datetime__gt=timezone.now(), id=slot_id
        )
        if not slots:
            raise errors.SlotNotFoundError(
                f'No upcoming slot found: {slot_id}'
            )
        slot = slots[0]

        # ensure student not in selected seminar
        if slot.students.filter(pk=student.pk).exists():
            raise errors.StudentAlreadyPresentError(
                f'Student {student} already in seminar {slot}'
            )
        return slot

    def send_reminder(self, connection: Any, reminder_type: str) -> None:
        """Send a reminder email to the student"""
        html_msg = render_to_string(
            'class_bookings/email/reminder.html',
            {'slot': self},
        )

        student_emails = [student.email for student in self.students.all()]
        email = EmailMultiAlternatives(
            subject="Reminder: Seminar %r" % self.seminar.title,
            body=strip_tags(html_msg),
            from_email=None,    # uses DEFAULT_FROM_EMAIl
            to=student_emails,
            connection=connection
        )
        email.attach_alternative(html_msg, 'text/html')
        email.send(fail_silently=False)

        # ensure marked as saved
        super().send_reminder(connection, reminder_type)


class IndividualSlot(BaseSlot):
    '''
    An individual slot bookable by a student

    Activity chosen upon booking by student
    '''
    lesson = models.ForeignKey(
        Activity,
        limit_choices_to={
            "activity_type": Activity.INDIVIDUAL,
            "is_bookable": True,
        },
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    student = models.ForeignKey(
        Student, on_delete=models.PROTECT, null=True, blank=True
    )


    def send_reminder(self, connection: Any, reminder_type: str) -> None:
        """Send a reminder email to the student"""
        email = EmailMessage(
            subject="Reminder: Seminar %r" % self.seminar.title,
            body="This is a reminder about your upcoming Polyglossa class!",
            from_email=None,    # uses DEFAULT_FROM_EMAIl
            to=[self.student.email],
            connection=connection
        )
        email.send(fail_silently=False)

        # ensure marked as saved
        super().send_reminder(connection, reminder_type)
