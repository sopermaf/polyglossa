"""
class_booking error definitions
"""

class ClassBookingError(Exception):
    """Base class class_bookings exceptions.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message, *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.message = message


class StudentAlreadyPresentError(ClassBookingError):
    """student already present in a slot"""


class UnpaidOrderError(ClassBookingError):
    """unpaid order of same type already exists"""


class SlotNotFoundError(ClassBookingError):
    """a slot meeting the search isn't present"""
