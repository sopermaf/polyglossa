'''Common Test Variables and methods for `class_bookings` module
'''
import class_bookings.models as models


def db_add_activity(title, activity, is_bookable=True, price=20):
    '''Add a lesson to test DB
    '''
    activity = models.Activity(
        activity_type=activity,
        title=title,
        price=price,
        is_bookable=is_bookable,
    )
    activity.save()
