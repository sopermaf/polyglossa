from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from class_bookings.models import Lesson, Student
from datetime import datetime as dt
import class_bookings.util as class_booking_utils
from class_bookings.validation import validate_lesson_request
import json

# Create your views here.
def postLesson(request):
    '''
    Receive a lesson post request,
    perform validation, and store
    the request if valid.

    Error returned if invalid request.
    '''
    lesson_request = {}
    for lessonInfoSection in class_booking_utils.LESSON_POST_KEYS:
        try:
            lesson_request[lessonInfoSection] = request.POST[lessonInfoSection]
        except KeyError:
            error_response = HttpResponse()
            error_response.status_code = class_booking_utils.BAD_REQUEST_CODE
            error_response.content = f"Missing {lessonInfoSection} to reserve lesson"
            return error_response
    
    # validate
    try:
        validate_lesson_request(lesson_request)
    except ValueError:
        print(f"Lesson Not Created: {lesson_request}")
        error_response = HttpResponse('Bad request')
        error_response.status_code = class_booking_utils.BAD_REQUEST_CODE
        return error_response

    # store Student and Lesson in DataBase
    student = Student(
                name=lesson_request[class_booking_utils.REQUEST_KEY_NAME],
                email=lesson_request[class_booking_utils.REQUEST_KEY_EMAIL],
            )
    student.save()
    
    lesson = Lesson(
                student=student,
                class_time=dt.strptime(
                    lesson_request[class_booking_utils.REQUEST_KEY_TIME],
                    class_booking_utils.FORMAT_LESSON_DATETIME
                ),
            )
    lesson.save()
    
    # TODO: add logging
    print(f"Lesson Created: {lesson}")

    success_response = HttpResponse('Student and Lesson created')
    success_response.status_code = class_booking_utils.RESOURCE_CREATED_CODE
    return success_response
