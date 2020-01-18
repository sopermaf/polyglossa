'''This is design of the tables that are used
in the database to manage the class_bookings
module
'''
from datetime import timedelta

from django.db import models
from .util import dt_to_str

# Create your models here.


class Student(models.Model):
    '''
    Represents a student taking lessons on the site.
    '''
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return f"{self.name}, {self.email}"

    @staticmethod
    def get_student_safe(email):
        '''Find a student by their email address.\n\n
        Returns `None` if Student doesn't exist
        '''
        try:
            student = Student.objects.get(
                email=email)  # pylint: disable=no-member
        except Student.DoesNotExist:    # pylint: disable=no-member
            student = None

        return student

    @staticmethod
    def get_existing_or_create(name, email):
        '''Adds to DB and returns new student
        if no student using `email` exists.
        '''
        student = Student.get_student_safe(email)
        if student is None:
            student = Student(
                name=name,
                email=email
            )
            student.save()
        return student


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
    activity_type = models.CharField(
        max_length=3,
        choices=ACTIVITY_TYPES,
        default=INDIVIDUAL,
    )
    title = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=1000, blank=True, default="")
    price = models.FloatField()
    is_bookable = models.BooleanField(default=False)

    def __str__(self):
        booking_status = "Bookable" if self.is_bookable else "Not Bookable"
        return f"({booking_status}) {self.activity_type} - {self.title} - ${self.price:.2f}"


class BaseSlot(models.Model):
    '''
    Defines a bookable slot for students to
    join
    '''
    start_datetime = models.DateTimeField('The lesson date and time')
    duration_in_mins = models.PositiveSmallIntegerField(default=60)

    @property
    def end_datetime(self):
        ''' Returns the end datetime of a lesson '''
        return self.start_datetime + timedelta(minutes=self.duration_in_mins)

    def __str__(self):
        return f"{dt_to_str(self.start_datetime)} ({self.duration_in_mins} mins)"


class SeminarSlot(BaseSlot):
    '''
    A seminar datetime slot bookable by a student

    Activity chosen upon slot creation by admin.
    '''
    seminar = models.ForeignKey(
        Activity,
        limit_choices_to={
            "activity_type": Activity.SEMINAR,
            "is_bookable": True,
        },
        on_delete=models.PROTECT,
    )
    students = models.ManyToManyField(Student, blank=True)


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
