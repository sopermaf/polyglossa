"""
Task related db models

Created due to lack of Celery support on pythonanywhere.com
"""
# pylint: disable=missing-class-docstring,too-few-public-methods
from django.db import models
from django.core.mail import send_mail


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


    def send(self):
        """Send email and mark task as complete"""
        send_mail(
            subject=self.subject,
            message=self.msg,
            from_email=None,    # uses DEFAULT_FROM_EMAIl
            recipient_list=[self.to_email],
        )

        self.sent = True
        self.save()

        print("Email sent to %r with subject %r" % (self.to_email, self.subject))
