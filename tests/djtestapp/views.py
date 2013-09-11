from django.template import Template as DjangoTemplate
from django.template.response import TemplateResponse
from jinja2.environment import Template as JinjaTemplate 


def django_template_view(request):
    return TemplateResponse(request, 'django.html', {
        'foo': { 'bar': 'baz' },
    })


def django_template_object(request):
    return TemplateResponse(request, DjangoTemplate('{{ snakes.spam }}\n'), {
        'snakes': { 'spam': 'eggs' },    
    })


def jinja_template_view(request):
    return TemplateResponse(request, 'jinja.html', {
        'add': lambda *a: sum(a),
        'foo': { 'bar': 'baz' },
    })


def jinja_template_object(request):
    template_body = '{{ riddles[0]["answer"] }}'
    return TemplateResponse(request, JinjaTemplate(template_body), {
        'riddles': [{ 'answer': 'teeth' }],
    })
