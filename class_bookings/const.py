'''
Keys and values that remain constant in class_bookings
'''
# request params
REQUEST_KEY_NAME = 'student_name'
REQUEST_KEY_EMAIL = 'student_email'
REQUEST_KEY_LESSON_CHOICE = ''
BOOKING_POST_KEYS = {
    REQUEST_KEY_NAME,
    REQUEST_KEY_EMAIL,
    REQUEST_KEY_LESSON_CHOICE,
}

# HTTP Codes used
BAD_REQUEST_CODE = 400
RESOURCE_CREATED_CODE = 201

# formats
FORMAT_BOOKING_DATETIME = '%Y-%m-%d %H:%M'

# url names
POST_LESSON_URL_NAME = 'create-individual'
SEMINAR_POST_NAME = 'create-seminar'
