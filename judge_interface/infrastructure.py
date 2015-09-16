from rest_framework.response import Response
from django.template.response import TemplateResponse


def template_result(func):
    def inner(self, request, *args, **kwargs):
        template, context = func(self, request, *args, **kwargs)
        return TemplateResponse(request, template, context)

    return inner


def json_result(func):
    def inner(self, request, *args, **kwargs):
        try:
            data = func(self, request, *args, **kwargs)
            return Response(data if data else {}, content_type='application/json')
        except Exception as ex:
            return Response({'error': str(ex)}, content_type='application/json')

    return inner
