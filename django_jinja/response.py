from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django import template
from django.template import defaultfilters
from django.template.context import get_standard_processors
from django.template.response import TemplateResponse
import jinja2


# set up the jinja template loaders
loaders = []
for path in getattr(settings, 'TEMPLATE_DIRS', []):
    loaders.append(jinja2.FileSystemLoader(path))
for app in getattr(settings, 'INSTALLED_APPS', []):
    loaders.append(jinja2.PackageLoader(app))


# create sensible defaults for the environment
env_kwargs = {
    'extensions': ['jinja2.ext.loopcontrols'],
    'line_comment_prefix': '# ',
    'loader': jinja2.ChoiceLoader(loaders),
    'trim_blocks': True,
}

# now, accept addendums to the environment from
# the Django settings...
env_kwargs.update(getattr(settings, 'JINJA_ENVIRONMENT', {}))

# okay, now create the jinja environment
env = jinja2.Environment(**env_kwargs)


# now set the globals and filters into the jinja
# environment...
env.globals = {
    'url': reverse,
    'range': xrange,
}
env.globals.update(getattr(settings, 'JINJA_GLOBALS', {}))

for f in ('capfirst', 'linebreaks', 'linebreaksbr', 'linenumbers', 'pluralize', 'removetags', 'slugify', 'striptags', 'timesince', 'timeuntil', 'title', 'truncatewords', 'truncatewords_html', 'unordered_list', 'urlize', 'urlizetrunc', 'yesno'):
    env.filters[f] = getattr(defaultfilters, f)
env.filters['format_date'] = defaultfilters.date
env.filters.update(getattr(settings, 'JINJA_FILTERS', {}))



class JinjaTemplateResponse(TemplateResponse):
    """Subclass of TemplateResponse that routes its response
    through the Jinja templating language rather than the Django
    stock templating language."""
    
    def resolve_context(self, context):
        if context:
            context = dict(context)
        else:
            context = {}
        
        # I still want to keep the use of my Django context processors
        # even though this is a Jinja template; therefore, process them manually
        for context_processor in get_standard_processors():
            new_stuff = context_processor(self._request)
            if new_stuff:
                context.update(dict(new_stuff))
    
        # return a flat dict; jinja doesn't have context objects
        return context
    
    def resolve_template(self, template):
        """Takes a template and tries to return back the appropriate
        Jinja template object.
        If an explicit Django template object is passed, do nothing."""
        
        if isinstance(template, basestring):
            return env.get_template(template)
        elif isinstance(template, (list, tuple)):
            return env.select_template(template)
        else:
            return template
