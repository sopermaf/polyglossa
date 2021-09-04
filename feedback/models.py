# pylint: missing-module-docstring
from django.db import models
from django.db.models.enums import Choices


# Create your models here.
class FeedbackType(models.Model):
    """Feedback subject enums"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return 'FeedbackType(name=%r)' % self.name


class Feedback(models.Model):
    """Client feedback on various polyglossa"""
    class Status(models.TextChoices):
        """Feedback status states"""
        OPEN = 'O'
        CLOSED = 'C'
        AWAITING_RESPONSE = 'W'
        ACTION_REQUIRED = 'A'

    feedback_type = models.ForeignKey(FeedbackType, on_delete=models.CASCADE)
    reference = models.CharField(max_length=100, blank=True, default='')
    status = models.CharField(
        max_length=1, choices=Status.choices, default=Status.OPEN)
    detail = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self) -> str:
        return 'Feedback(feedback_type={!r}, reference={!r}, detail={!r})'.format(
            self.feedback_type,
            self.reference,
            self.detail,
        )
