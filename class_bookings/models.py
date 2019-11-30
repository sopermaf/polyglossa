'''This is design of the tables that are used
in the database to manage the class_bookings
module
'''
from django.db import models

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
            student = Student.objects.get(email=email)  # pylint: disable=no-member
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


class LessonType(models.Model):
    '''A polyglossa lesson that
    that is offered for booking.
    '''
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, unique=True)
    price = models.FloatField()                 # form for adding to make always positive?
    isBookable = models.BooleanField(default=False)
    description = models.CharField(max_length=1000, blank=True, default="")

    def __str__(self):
        return f"{self.title} - ${self.price}\nIs Bookable:{self.isBookable}"


class Booking(models.Model):
    '''This is meant to represent 1-to-1
    bookings made by an individual student
    for a private class on polyglossa.
    '''
    AWAITING_PAYMENT = 'AWAITING PAYMENT'
    HAS_PROBLEM = 'PROBLEM'
    CANCELLED_NOT_PAID = 'NOT PAID'
    CANCELLED_REFUNDED = 'REFUNDED'
    CONFIRMED_UPCOMING = 'UPCOMING'
    COMPLETED_NORMAL = 'COMPLETED'
    COMPLETED_DEFAULT_PAID = 'COMP_TEACHER_PAID'
    STATUS_CHOICES = [
        (AWAITING_PAYMENT, 'Awaiting Payment for booking'),
        (CONFIRMED_UPCOMING, 'Upcoming lesson with confirmed payment'),
        (HAS_PROBLEM, 'Booking in problem state and requires attention'),
        (CANCELLED_NOT_PAID, 'Lesson cancelled before payment'),
        (CANCELLED_REFUNDED, 'Lesson cancelled and refunded'),
        (COMPLETED_NORMAL, 'Lesson successfully completed'),
        (COMPLETED_DEFAULT_PAID,
         'Considered completed. Teacher paid for lesson by default'),
    ]
    # model fields
    id = models.AutoField(primary_key=True)
    lesson_datetime = models.DateTimeField('The lesson date and time')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=AWAITING_PAYMENT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    lessonType = models.ForeignKey(LessonType, on_delete=models.PROTECT)

    def __str__(self):
        return "Time:{}\nDetails: {} - ${}\nStudent: {} - {}\nStatus: {}".format(
            self.lesson_datetime,   # pylint: disable=no-member
            self.lessonType.title,  # pylint: disable=no-member
            self.lessonType.price,  # pylint: disable=no-member
            self.student.name,      # pylint: disable=no-member
            self.student.email,     # pylint: disable=no-member
            self.status,
        )
