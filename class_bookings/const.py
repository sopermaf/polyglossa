'''
Keys and values that remain constant in class_bookings
'''
# request params
KEY_NAME = 'student_name'
KEY_EMAIL = 'student_email'
KEY_CHOICE = 'booking_id'
BOOKING_PARAMS = {
    KEY_NAME,
    KEY_EMAIL,
    KEY_CHOICE,
}

# HTTP Codes used
BAD_REQUEST_CODE = 400
RESOURCE_CREATED_CODE = 201
SUCCESS_CODE = 200

# formats
FORMAT_BOOKING_DATETIME = '%Y-%m-%d %H:%M'

# url names
SEMINAR_POST_NAME = 'signup-seminar'
