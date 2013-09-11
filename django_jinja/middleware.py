from django.conf import settings
from django_jinja.response import JinjaTemplateResponse
import re


class JinjaMiddleware(object):
    """Middleware that substitutes in a Jinja template to TemplateResponse
    unless asked not to.
    """
    def process_template_response(self, request, response):
        # Sanity check: The admin uses the regular Django template engine.
        # 
        # Also, the user may have URLs to exclude from this -- allow for
        # these. The default shall be `^/admin/`, which excludes the admin
        # if it's set at the normal URL; the user will have to change it if 
        # it's located elsewhere.
        exclude_paths = getattr(settings, 'JINJA_EXCLUDE_PATHS', [r'^/admin/'])
        for path in exclude_paths:
            if re.search(path, request.path):
                return response
        
        # Return a jinja template response...
        return JinjaTemplateResponse(
            request, response.template_name, response.context_data, 
            content_type=response['Content-Type'],
            status=response.status_code,
        )
