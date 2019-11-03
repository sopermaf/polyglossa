from django.db import models

# Create your models here.
class Student(models.Model):
    '''
    Represents a student taking lessons on the site.
    '''
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.name}, {self.email}"


class Lesson(models.Model):
    '''
    A polyglossa 1-on-1 lesson
    '''
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_time = models.DateTimeField('The lesson time')
    completed = models.BooleanField(default=False)
    price = models.FloatField(default=20)

    def __str__(self):
        return f"{self.student} - {self.class_time} - {self.price} - Done: {self.completed}"
