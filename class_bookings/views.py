from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json

# Create your views here.
def make_booking(request):
    '''
    Receive a POST request and
    store this booking as a Lesson
    '''
    post_keys = [
        'student_name',
        'student_email',
        'lesson_time'
    ]
    student_data = {}
    for key in post_keys:
        try:
            student_data[key] = request.POST[key]
        except KeyError:
            error_response = HttpResponse()
            error_response.status_code = 400 # bad request
            error_response.content = f"Missing {key} to reserve class"
            return error_response
    

    return JsonResponse(student_data)
