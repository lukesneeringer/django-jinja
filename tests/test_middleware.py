from __future__ import unicode_literals
from django.test import Client, RequestFactory
from django_jinja.response import JinjaTemplateResponse
import unittest


class MiddlewareSuite(unittest.TestCase):
    """A test suite for testing that the Django-Jinja middleware
    functions in the expected manner.
    """
    def test_jinja_template(self):
        """Test that a TemplateResponse that should become a Jinja
        template does, in fact, do so.
        """
        client = Client()
        response = client.get('/jinja-template.html')
        self.assertEqual(response.content, '12\nbaz'.encode('utf8'))

    def test_django_template(self):
        """Test that a TemplateResponse that should become a Django
        template does, in fact, do so.
        """
        client = Client()
        response = client.get('/django-template.html')
        self.assertEqual(response.content, 'baz\n'.encode('utf8'))

    def test_django_template_object(self):
        """Test that sending an actual Django template object
        to TemplateResponse returns that template object unscathed.
        """
        client = Client()
        response = client.get('/template-object-django.html')
        self.assertEqual(response.content, 'eggs\n'.encode('utf8'))

    def test_jinja_template_object(self):
        """Test that sending a Jinja template object to TemplateResponse
        returns that template object unscathed.
        """
        client = Client()
        response = client.get('/template-object-jinja.html')
        self.assertEqual(response.content, 'teeth'.encode('utf8'))


class ResponseSuite(unittest.TestCase):
    """A test suite to establish that the JinjaTemplateResponse
    object functions as expected.
    """
    def setUp(self):
        self.rf = RequestFactory()

    def test_no_context(self):
        """Establish that sending an empty context works as expected,
        instantiating an empty dict and then populating it with context
        processors, if any.
        """
        req = self.rf.get('/foo')
        response = JinjaTemplateResponse(req, 'empty.html')
        content = response.rendered_content
        self.assertIsInstance(response.context_data, dict)
        self.assertEqual(content, '')

    def test_template_list(self):
        """Establish that a list of templates is processed correctly,
        with the first valid match chosen.
        """
        req = self.rf.get('/foo')
        response = JinjaTemplateResponse(req, ['bogus.html', 'jinja.html'], {
            'add': lambda *a: sum(a),
            'foo': { 'bar': 'spam' },
        })
        response.render()
        self.assertEqual(response.content, '12\nspam'.encode('utf8'))

    def test_invalid_template(self):
        """Establish that an invalid object being sent down as a
        template raises TypeError.
        """
        req = self.rf.get('/foo')
        with self.assertRaises(TypeError):
            response = JinjaTemplateResponse(req, object())
            response.render()
