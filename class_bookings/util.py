'''
This file is the central resource for defining 
constants and common util functions in class_bookings
'''

# request params
REQUEST_KEY_TIME = 'lesson_time'
REQUEST_KEY_NAME = 'student_name'
REQUEST_KEY_EMAIL = 'student_email'

LESSON_POST_KEYS = [
    REQUEST_KEY_TIME,
    REQUEST_KEY_NAME,
    REQUEST_KEY_EMAIL,
]

# formats
FORMAT_DB_DATETIME = '%Y-%m-%d %H:%M:%S'
FORMAT_LESSON_DATETIME = '%Y-%m-%d %H:%M'

# url names
POST_LESSON_URL_NAME = 'create-booking'
