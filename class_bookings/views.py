from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from class_bookings.models import LessonType, Student, Booking
from datetime import datetime as dt
import class_bookings.util as cb_utils
from class_bookings.validation import validate_booking_request
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
    for lessonInfoSection in cb_utils.BOOKING_POST_KEYS:
        try:
            lesson_request[lessonInfoSection] = request.POST[lessonInfoSection]
        except KeyError:
            error_response = HttpResponse()
            error_response.status_code = cb_utils.BAD_REQUEST_CODE
            error_response.content = f"Missing {lessonInfoSection} to reserve lesson"
            return error_response
    
    # validate
    try:
        validate_booking_request(lesson_request)
    except ValueError:
        print(f"Lesson Not Created: {lesson_request}")
        error_response = HttpResponse('Bad request')
        error_response.status_code = cb_utils.BAD_REQUEST_CODE
        return error_response

    #TODO:remove this logic from main
    existingStudent = Student.getStudentSafe(
                        lesson_request[cb_utils.REQUEST_KEY_EMAIL]
                      )
    if existingStudent is None:
        student = Student(
                    name=lesson_request[cb_utils.REQUEST_KEY_NAME],
                    email=lesson_request[cb_utils.REQUEST_KEY_EMAIL],
                )
        student.save()
    else:
        student = existingStudent

    # TODO: add tests and exception handling for this section
    lesson = LessonType.objects.get(
                    title=lesson_request[cb_utils.REQUEST_KEY_LESSON_CHOICE]
            )


    booking = Booking(
                student=student,
                lessonType=lesson,
                lesson_datetime=dt.strptime(
                    lesson_request[cb_utils.REQUEST_KEY_TIME],
                    cb_utils.FORMAT_BOOKING_DATETIME
                ),
            )
    booking.save()
    
    # TODO: add logging
    print(f"Lesson Created: {booking}")

    success_response = HttpResponse('Student and Lesson created')
    success_response.status_code = cb_utils.RESOURCE_CREATED_CODE
    return success_response
