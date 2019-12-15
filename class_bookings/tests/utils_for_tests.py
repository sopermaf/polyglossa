'''Common Test Variables and methods for `class_bookings` module
'''
import class_bookings.models as models

def add_lesson_type_db(title, is_bookable, price=20):
    '''Add a lesson to test DB
    '''
    lesson_type = models.LessonType(
        title=title,
        price=price,
        isBookable=is_bookable,
    )
    lesson_type.save()
