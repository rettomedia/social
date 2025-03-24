from django.http import HttpResponseNotFound
from django.template.loader import render_to_string

class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404:
            return HttpResponseNotFound(render_to_string('404.html'))

        return response
