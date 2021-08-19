# pylint: missing-class-docstring, missing-module-docstring
from django.contrib import admin

from . import models


admin.register(models.FeedbackType)
admin.register(models.Feedback)
