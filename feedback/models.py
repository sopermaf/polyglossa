# pylint: missing-module-docstring
from django.db import models

# Create your models here.
class FeedbackType(models.Model):
    """Feedback subject enums"""
    name = models.CharField(max_length=100)


class Feedback(models.Model):
    """Client feedback on various polyglossa"""
    feedback_type = models.ForeignKey(FeedbackType, on_delete=models.CASCADE)
    reference = models.CharField(max_length=100, blank=True, default='')
    detail = models.TextField()
