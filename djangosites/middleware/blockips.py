"""
simple middlware to block IP addresses via settings variable BLOCKED_IPS
http://djangosnippets.org/snippets/744/
"""
from django.conf import settings
from django import http

class BlockedIpMiddleware(object):

    def process_request(self, request):
        if request.META['REMOTE_ADDR'] in settings.BLOCKED_IPS:
            return http.HttpResponseForbidden('<h1>Forbidden</h1>')
        return None

