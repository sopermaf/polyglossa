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
    def getStudentSafe(email):
        '''Find a student by their email address.\n\n
        Returns `None` if Student doesn't exist
        '''
        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            student = None

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
    student = models.ForeignKey(Student, on_delete=models.CASCADE)        # TODO: review this behaviour
    lessonType = models.ForeignKey(LessonType, on_delete=models.CASCADE)  # TODO: review this behaviour

    def __str__(self):
        return "Time:{}\nDetails: {} - ${}\nStudent: {} - {}\nStatus: {}".format(
            self.lesson_datetime,
            self.lessonType.title,
            self.lessonType.price,
            self.student.name,
            self.student.email,
            self.status,
        )
