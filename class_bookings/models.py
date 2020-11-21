'''This is design of the tables that are used
in the database to manage the class_bookings
module
'''
# pylint: disable=unused-variable

import uuid
import datetime

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models

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
    description = models.CharField(max_length=1000, blank=True, default="")
    price = models.FloatField()
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


class BaseSlot(models.Model):
    '''
    Defines a bookable slot for students to
    join
    '''
    start_datetime = models.DateTimeField('The lesson date and time', )
    duration_in_mins = models.PositiveSmallIntegerField(default=60)

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


class SeminarSlot(BaseSlot):
    '''
    A seminar datetime slot bookable by a student

    Activity chosen upon slot creation by admin.
    '''
    external_id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4()
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

    # def save(self, *args, **kwargs):
    #     if not self.external_id:
    #         self.external_id = uuid.uuid4()
    #     super(self).save(*args, **kwargs)

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
