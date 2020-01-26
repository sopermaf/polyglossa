'''
This file is the central resource for defining
constants and common util functions in class_bookings
'''
from django.http import HttpResponse

from . import const


# RESPONSES


def http_bad_request(msg="Bad Request"):
    '''Creates a HTTP response
    code `BAD_REQUEST_CODE`
    '''
    error_response = HttpResponse(
        msg,
        status=const.BAD_REQUEST_CODE,
    )
    return error_response


def http_resource_created(msg="Resource created successfully"):
    '''Returns a HTTP response with code
    `RESOURCE_CREATED_CODE`
    '''
    return HttpResponse(
        msg,
        status=const.RESOURCE_CREATED_CODE,
    )
