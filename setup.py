# -*- encoding: utf8 -*-

import os

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

classifiers = ["Programming Language :: Python", "Framework :: Pyramid",
               "Topic :: Internet :: WWW/HTTP",
               "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
               ]

requires = [
    # WSGI:
    'waitress',
    # Pyramid:
    'pyramid',
    'pyramid_chameleon',
    'pyramid_layout',
    'pyramid_tm',
    'pyramid_beaker',
    # Debug:
    'pyramid_debugtoolbar',
    'ppretty',
    # I18N:
    'lingua',
    'Babel',
    # SQL:
    'pg8000',
    'SQLAlchemy >= 1.1.3',
    'transaction',
    'alembic >= 0.8.8',
    'zope.sqlalchemy',
    # Cryptography:
    'bcrypt',
    # HTTP:
    'requests',
]

entry_points = """
[paste.app_factory]
main = muuri:main
"""

setup(author = u'Pekka Järvinen',
      name = 'muuri',
      version = '0.1',
      description = 'muuri',
      long_description = 'muuri',
      classifiers = classifiers,
      author_email = 'pekka.jarvinen@gmail.com',
      url = 'https://raspi.github.io/projects/muuri/',
      keywords = 'web pyramid python',
      packages = find_packages(),
      include_package_data = True,
      zip_safe = False,
      install_requires = requires,
      tests_require = requires,
      test_suite = "muuri",
      entry_points = entry_points,
      )
