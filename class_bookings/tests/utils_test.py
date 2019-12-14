'''Common Test Variables and methods for `class_bookings` module
'''
import class_bookings.models as models

def add_lesson_type_db(title, is_bookable):
    '''Add a lesson to test DB
    '''
    lesson_type = models.LessonType(
        title=title,
        price=20,
        isBookable=is_bookable,
    )
    lesson_type.save()
