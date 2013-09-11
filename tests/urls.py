from __future__ import absolute_import, unicode_literals
from django.conf.urls import include, patterns, url


urlpatterns = patterns('tests.djtestapp.views',
    url(r'jinja-template\.html', 'jinja_template_view'),
    url(r'django-template\.html', 'django_template_view'),
    url(r'template-object-django\.html', 'django_template_object'),
    url(r'template-object-jinja\.html', 'jinja_template_object'),
)
