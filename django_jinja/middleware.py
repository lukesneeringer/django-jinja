from django_jinja.response import JinjaTemplateResponse


class JinjaMiddleware(object):
    def process_template_response(self, request, response):
        # sanity check: the admin uses the regular django template engine;
        # allow for this sloppily by checking for the /admin/ urls...
        if request.path.startswith('/admin/'):
            return response
        
        # return a jinja template response...
        return JinjaTemplateResponse(
            request, response.template_name, response.context_data, 
            content_type=response['Content-Type'],
            status=response.status_code,
        )