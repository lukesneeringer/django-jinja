django-jinja-middleware
=======================

This package installs `django_jinja`, which is a tiny Python package that,
when installed as middleware in any Django application, will cause the Jinja2
templating engine to be used in lieu of the stock Django templating language,
provided you used a `TemplateResponse` in your Django view.

It works with Django 1.4 or up. It will *mostly* work with Django 1.3 as well,
but some stock Django views (such as the built-in login view) weren't changed
to use `TemplateResponse` until Django 1.4.


Installing
==========

Install the package using pip:

    sudo pip install django-jinja-middleware
    
Then install as middleware in your Django settings file by
adding the following class to your `MIDDLEWARE_CLASSES`:

    MIDDLEWARE_CLASSES = (
        [...],
        'django_jinja.middleware.JinjaMiddleware',
    )
    
That's it!