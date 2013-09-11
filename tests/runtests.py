import os
import sys
import unittest


# Ensure that the django_jinja directory is part of our Python path.
APP_ROOT = os.path.realpath(os.path.dirname(__file__) + '/../')
sys.path.append(APP_ROOT)

# Point to our settings module.
os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'


def load_tests(loader, standard_tests, throwaway):
    return loader.discover('tests')


if __name__ == '__main__':
    unittest.main()
