import json

from django.core.handlers.asgi import ASGIRequest
from django.http.response import HttpResponseServerError


class JsonErrorResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: ASGIRequest):
        response: HttpResponseServerError = self.get_response(request)

        if response.headers.get("Content-Type", default="") != "application/json":
            if str(response.status_code).startswith("4"):
                response.content = json.dumps(
                    {"detail": "Client error has been occurred."}
                )
                response.headers["Content-Type"] = "application/json"

            elif str(response.status_code).startswith("5"):
                response.content = json.dumps(
                    {"detail": "Server error has been occurred."}
                )
                response.headers["Content-Type"] = "application/json"

        return response
