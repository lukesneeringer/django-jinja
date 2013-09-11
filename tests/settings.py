import os
import sys


DEBUG = False
TEMPLATE_DEBUG = DEBUG


# Database settings. This assumes that the default user and empty
# password will work.
#
# Note: This isn't actually used.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
        'NAME': 'django_jinja',
    }
}


# Boilerplate settings.
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_DIRS = ()
SECRET_KEY = '945iu@*yn_k_+c&4&i#q8$meuvg_u4x3dsne6ei3h+#!lt3a=@'


# Installed apps. Be smart about this: search for things under the
# `tests/` directory, but add them as applications as they have their
# own models that we need in order to test this stuff.
INSTALLED_APPS = (
    'tests.djtestapp',
)


# The root URL configuration.
ROOT_URLCONF = 'tests.urls'


# Middleware classes; this is where django-jinja is fundamentally
# "installed".
MIDDLEWARE_CLASSES = (
    'django_jinja.middleware.JinjaMiddleware',
)


# Template directories
APP_ROOT = os.path.realpath(os.path.dirname(__file__) + '/../')
TEMPLATE_DIRS = (APP_ROOT + '/tests/templates/',)

# Django/Jinja settings
JINJA_EXCLUDE_PATHS = (
    r'^/django',
)
