'''These are the request handlers for the class_bookings
section of the polyglossa website.
'''
from django.views.decorators.csrf import csrf_exempt

from . import models

@csrf_exempt
def seminar_booking(request):
    '''
    Process a request from the the form
    and add a student to the selected student
    '''
    # get the info
    # validate
    # save and respond
    return request
