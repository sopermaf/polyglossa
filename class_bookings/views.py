from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from class_bookings.models import Lesson, Student
from datetime import datetime as dt
import class_bookings.util as cb
from class_bookings.validation import validate_lesson_request
import json

# Create your views here.
def make_booking(request):
    '''
    Receive a POST request and
    store this booking as a Lesson
    '''
    post_keys = [
        cb.REQ_NAME,
        cb.REQ_EMAIL,
        cb.REQ_TIME,
    ]
    lesson_request = {}
    for key in post_keys:
        try:
            lesson_request[key] = request.POST[key]
        except KeyError:
            error_response = HttpResponse()
            error_response.status_code = 400 # bad request
            error_response.content = f"Missing {key} to reserve lesson"
            return error_response
    
    # validate
    validate_lesson_request(lesson_request)
    #raise ValueError('problem with values')

    # store Student and Lesson in DataBase
    student = Student(
                name=lesson_request[cb.REQ_NAME],
                email=lesson_request[cb.REQ_EMAIL],
            )
    student.save()
    lesson = Lesson(
                student=student,
                class_time=dt.strptime(
                    lesson_request[cb.REQ_TIME],
                    cb.FORMAT_TIME
                ),
            )
    lesson.save()
    
    # should create a log file
    print(f"Lesson Created: {lesson}")

    return JsonResponse(lesson_request)
