from __future__ import unicode_literals

from django.core.urlresolvers import resolve
from django.contrib.auth.middleware import AuthenticationMiddleware as DjangoAuthenticationMiddleware
from django.contrib.auth import get_user
from django.http.response import HttpResponseRedirect, HttpResponse, Http404
from django.core.exceptions import ValidationError
from django.utils.encoding import force_text
from django.utils.translation import ugettext
from django.conf import settings

from is_core.exceptions import ResponseException
from is_core.exceptions.response import responseexception_factory


class RequestKwargsMiddleware(object):

    def process_request(self, request):
        request.kwargs = resolve(request.path).kwargs


# Not working with pyston exceptions
class HTTPExceptionsMiddleware(object):

    def process_exception(self, request, exception):
        if isinstance(exception, ResponseException):
            return exception.get_response(request)
        if isinstance(exception, ValidationError):
            return responseexception_factory(request, 422, ugettext('Unprocessable Entity'), exception.messages)
        if not settings.DEBUG and isinstance(exception, Http404):
            return responseexception_factory(request, 404, ugettext('Not Found'), force_text(exception))
