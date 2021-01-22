# pylint: disable=missing-module-docstring,import-outside-toplevel,unused-import
from django.apps import AppConfig


class PaymentsConfig(AppConfig): # pylint: disable=missing-class-docstring
    name = 'payments'

    def ready(self):
        from . import signals
