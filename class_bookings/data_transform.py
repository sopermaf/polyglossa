'''This is a model to perform operations on DB
data and to maintain the operations of data retrieval
separate from the models and views
'''
import class_bookings.models as models


def get_bookable_lesson_details():
    '''Returns a list of strings with
    the title and price of all bookable
    `LessonType`
    '''
    bookable_lessons = models.LessonType.objects.filter(isBookable=True)
    return ["%s (USD$%.2f)" % (lesson.title, lesson.price) for lesson in bookable_lessons]
