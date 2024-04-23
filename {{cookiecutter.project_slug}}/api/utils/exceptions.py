from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.status import is_success
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Get the default error response.
    response = exception_handler(exc, context)

    # Reformat error response message
    if response is not None:
        # Return a dictionary of errors if there are serializer errors
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            response.data = {"field_errors": response.data}
        # Rename "detail" key to "error" for consistency
        if not is_success(response.status_code) and "detail" in response.data:
            response.data["error"] = response.data.pop("detail")

    return response


class ServiceUnavailable(APIException):
    """Generic service unavailable exception"""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "Service temporarily unavailable, try again later."
    default_code = "service_unavailable"
