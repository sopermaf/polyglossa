"""
Task related db models

Created due to lack of Celery support on pythonanywhere.com
"""
# pylint: disable=missing-class-docstring,too-few-public-methods
from django.db import models
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


class UnsentEmailManager(models.Manager):
    def get_queryset(self): # pylint: disable=missing-function-docstring
        return super().get_queryset().filter(sent=False)


class EmailTask(models.Model):
    to_email = models.EmailField()
    subject = models.CharField(max_length=100)
    msg = models.TextField()
    sent = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    unsent = UnsentEmailManager()

    class Meta:
        ordering = ['-modified', '-created']


    def send(self, connection):
        """Send the email task and mark as sent"""
        email = EmailMultiAlternatives(
            subject=self.subject,
            body=strip_tags(self.msg),
            from_email=None,    # uses DEFAULT_FROM_EMAIl
            to=[self.to_email],
            connection=connection
        )
        email.attach_alternative(self.msg, 'text/html')

        email.send(fail_silently=False)

        self.sent = True
        self.save()
