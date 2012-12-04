from django.conf import settings
from django_jinja.response import JinjaTemplateResponse
import re


class JinjaMiddleware(object):
    def process_template_response(self, request, response):
        # sanity check: the admin uses the regular django template engine;
        # also, the user may have URLs to exclude from this -- allow for those
        # the default shall be ^/admin/, which excludes the admin if it's
        #   set at the normal URL; the user will have to change it if it's located
        #   elsewhere...
        exclude_paths = getattr(settings, 'JINJA_EXCLUDE_PATHS', [r'^/admin/'])
        for path in exclude_paths:
            if re.search(path, request.path):
                return response
        
        # return a jinja template response...
        return JinjaTemplateResponse(
            request, response.template_name, response.context_data, 
            content_type=response['Content-Type'],
            status=response.status_code,
        )