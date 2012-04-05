#!/usr/bin/env python
from setuptools import setup

setup(
    name='django_jinja_middleware',
    version='1.0',
    author='Luke Sneeringer',
    author_email='lukesneeringer@gmail.com',
    url='http://github.com/lukesneeringer/django-jinja-mw/',
    
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
