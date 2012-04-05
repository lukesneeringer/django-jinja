#!/usr/bin/env python
from setuptools import setup

setup(
    name='django_jinja_middleware',
    version='1.0.2',
    description='Django middleware class that takes TemplateResponses and renders them with Jinja, instead of the Django stock templating language.',
    author='Luke Sneeringer',
    author_email='lukesneeringer@gmail.com',
    url='http://github.com/lukesneeringer/django-jinja/',
    
    # what to install
    packages=['django_jinja'],
    
    # searches and classifications
    keywords='django,jinja,middleware',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    
    # dependencies
    install_requires=[
        'django >= 1.4',
        'jinja2 >= 2.6',
    ],
)
