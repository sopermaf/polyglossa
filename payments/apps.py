# pylint: disable=missing-module-docstring
from django.apps import AppConfig


class PaymentsConfig(AppConfig): # pylint: disable=missing-class-docstring
    name = 'payments'

    def ready(self):
        from . import signals   # pylint: disable=unused-import,import-outside-toplevel
