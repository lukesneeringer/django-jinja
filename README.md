django-jinja-middleware
=======================

This package installs `django_jinja`, which is a tiny Python package that,
when installed as middleware in any Django application, will cause the Jinja2
templating engine to be used in lieu of the stock Django templating language,
provided you used a `TemplateResponse` in your Django view.

It works with Django 1.4 or up. It will *mostly* work with Django 1.3 as well,
but some stock Django views (such as the built-in login view) weren't changed
to use `TemplateResponse` until Django 1.4.

All unit tests against Django 1.4.2 still pass when this middleware is installed,
even those that use particular templates.


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


Customizing Jinja
=================

Environment
-----------

The `django_jinja` package sets some sensible default settings for the Jinja engine.
In particular, it will introspect the template loaders and the context processors
given in the Django settings (`TEMPLATE_LOADERS`, `TEMPLATE_CONTEXT_PROCESSORS`, respectively)
and install them in their equivalent forms in Jinja.

In addition, `django_jinja` will default to adding a `line_comment_prefix` option of `# `
(that's a hash mark, then space), set the loop controls to on (adding the `continue` and `break`
tags, if you want them), and set `trim_blocks` to `True`.

To make changes to this at the project level, add `JINJA_ENVIRONMENT` to your settings file,
and set it as a dictionary mapping of the keyword arguments to be passed to the Jinja2.Environment
callable. Any keyword arguments you specify will override the defaults noted above.


Globals
-------

The `django_jinja` package will add two globals to your templates. The first is `url`, which
is a reference to `django.core.urlresolvers.reverse`. The second is `range`, which maps
to the Python 2 `xrange`.

To add globals at the project level, add a `JINJA_GLOBALS` dictionary to your settings file.
If you specify a global that is set by `django_jinja`, yours wins.


Other Configuration
-------------------

The `django_jinja` package listens to one additional setting:

### JINJA_EXCLUDE_PATHS

The `JINJA_EXCLUDE_PATHS` setting provides a list of regular expressions which,
if the value of `request.path` matches _any_ of them, the middleware will simply do
nothing (pass the response through).

By default, this is set to `['^/admin/']`, since the Django admin uses its own
Django templates, and is generally installed to that URL. If your admin is located elsewhere,
or if you need to exclude other paths from this behavior, simply set this setting.


Filters
-------

The `django_jinja` package will add a subset of Django's filters to maximize convenience.
The filters that are automatically added are:

  * capfirst
  * date (renamed to `format_date`)
  * linebreaks
  * linebreaksbr
  * linenumbers
  * pluralize
  * removetags
  * slugify
  * striptags
  * timesince
  * timeuntil
  * title
  * truncatewords
  * truncatewords\_html
  * unordered\_list
  * urlize
  * urlizetrunc
  * yesno
  
All of these retain their original names except `date`, which is now renamed to `format_date`.

You can add additional filters, or override the ones we've added, by adding a `JINJA_FILTERS` dictionary
to your Django settings file. If you specify a filter that the `django_jinja` specifies (the list above),
then yours wins.


Contact
=======

  * Luke Sneeringer
  * Email: lukesneeringer@gmail.com
  * Twitter: @lukesneeringer
  * GitHub: github.com/lukesneeringer