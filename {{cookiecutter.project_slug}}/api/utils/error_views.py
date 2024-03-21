from django.http import JsonResponse
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR


def server_error(request, *args, **kwargs):
    """Generic 500 error handler"""
    data = {"error": "Something went wrong"}
    return JsonResponse(data, status=HTTP_500_INTERNAL_SERVER_ERROR)


def bad_request(request, exception, *args, **kwargs):
    """Generic 400 error handler"""
    data = {"error": "Bad Request"}
    return JsonResponse(data, status=HTTP_400_BAD_REQUEST)
