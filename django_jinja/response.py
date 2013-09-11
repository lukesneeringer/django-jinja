from __future__ import absolute_import, unicode_literals
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django import template
from django.template import defaultfilters, Template as DjangoTemplate
from django.template.context import get_standard_processors
from django.template.response import TemplateResponse
from django.test.signals import template_rendered
from django.test.utils import instrumented_test_render as test_mode_render
from jinja2.environment import Template as JinjaTemplate
import jinja2
import six


class JinjaTemplateResponse(TemplateResponse):
    """Subclass of TemplateResponse that routes its response
    through the Jinja templating language rather than the Django
    stock templating language.
    """
    @property
    def _environment(self):
        # Set up the jinja template loaders.
        loaders = []
        for path in getattr(settings, 'TEMPLATE_DIRS', []):
            loaders.append(jinja2.FileSystemLoader(path))
        for app in getattr(settings, 'INSTALLED_APPS', []):
            loaders.append(jinja2.PackageLoader(app))

        # Create sensible defaults for the environment.
        env_kwargs = {
            'extensions': ['jinja2.ext.loopcontrols'],
            'line_comment_prefix': '# ',
            'loader': jinja2.ChoiceLoader(loaders),
            'trim_blocks': True,
        }

        # Now, accept addendums to the environment from
        # the Django settings...
        env_kwargs.update(getattr(settings, 'JINJA_ENVIRONMENT', {}))

        # okay, now create the jinja environment
        env = jinja2.Environment(**env_kwargs)


        # Now set the globals into the jinja environment.
        env.globals = {
            'url': reverse,
            'range': six.moves.range,
        }
        env.globals.update(getattr(settings, 'JINJA_GLOBALS', {}))

        # Now do the same for filters.
        for f in (  'capfirst', 'linebreaks', 'linebreaksbr', 'linenumbers',
                    'pluralize', 'removetags', 'slugify', 'striptags',
                    'timesince', 'timeuntil', 'title', 'truncatewords',
                    'truncatewords_html', 'unordered_list', 'urlize',
                    'urlizetrunc', 'yesno'  ):
            env.filters[f] = getattr(defaultfilters, f)
        env.filters['format_date'] = defaultfilters.date
        env.filters.update(getattr(settings, 'JINJA_FILTERS', {}))

        # Return the environment object.
        return env

    @property
    def rendered_content(self):
        """Return the freshly rendered content for the template and context
        described by this JinjaTemplateResponse object.
        """
        # First, get us the template object.
        template = self.resolve_template(self.template_name)

        # Sanity check: if this is a **Django** template object, then I
        # just want to go through superclass' system.
        if isinstance(template, DjangoTemplate):
            super_ = super(JinjaTemplateResponse, self)
            context = super_.resolve_context(self.context_data)
        else:
            context = self.resolve_context(self.context_data)

        # Now render the template and return the content.
        content = template.render(context)

        return content

    def resolve_context(self, context):
        """Change the context object into a dictionary (what Jinja uses),
        and go through all our context processors from settings."""

        # Get me a dictionary.
        if context:
            self.context_data = dict(context)
        else:
            self.context_data = {}
        
        # I still want to keep the use of my Django context processors
        # even though this is a Jinja template; therefore, process
        # them manually.
        for context_processor in get_standard_processors():
            new_stuff = context_processor(self._request)
            if new_stuff:
                self.context_data.update(dict(new_stuff))
    
        # Return a flat dict; jinja doesn't have context objects.
        return self.context_data
    
    def resolve_template(self, template):
        """Takes a template and tries to return back the appropriate
        Jinja template object.

        If an explicit Django template object is passed, do nothing.
        """
        # Sanity check: if I got an explicit Django template object,
        # I don't want to do anything at all.
        if isinstance(template, DjangoTemplate):
            return template

        # Sanity check: what if I get a **Jinja** template?
        # Don't do anything to that either.
        if isinstance(template, JinjaTemplate):
            return template

        # Okay, if I have a string or iterable, then figure out the right
        # template and return it.
        if isinstance(template, six.string_types):
            return self._environment.get_template(template)
        elif isinstance(template, (list, tuple)):
            return self._environment.select_template(template)

        # Something is wrong; stop.
        raise TypeError('Unrecognized object sent as a template: {0}.'.format(
            type(template).__name__,
        ))
