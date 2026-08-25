from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def friendly_exception_handler(exc, context):
    """
    Spec section 36: friendly error messages instead of raw stack traces,
    consistent shape across 400/401/403/404/409/422/500.
    """
    response = exception_handler(exc, context)

    if response is not None:
        detail = response.data
        if isinstance(detail, dict) and "detail" in detail:
            message = detail["detail"]
        elif isinstance(detail, dict):
            # field-level validation errors — keep them, but add a friendly summary
            message = "Please check the highlighted fields."
        else:
            message = str(detail)
        response.data = {
            "detail": message,
            "errors": detail if isinstance(detail, dict) else None,
            "status": response.status_code,
        }
        return response

    # Unhandled exceptions -> friendly 500 instead of leaking internals
    return Response(
        {"detail": "Something went wrong on our end. Please try again.", "status": 500},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
