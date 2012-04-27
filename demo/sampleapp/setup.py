import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'pyramid_tm',
    'pyramid_formalchemy',
    'pyramid_fanstatic',
    'fa.jquery',
    'pyramid_jinja2',
    'mako',
    'pyramid_debugtoolbar',
    'waitress',
    ]

setup(name='sampleapp',
      version='0.0',
      description='sampleapp',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='sampleapp',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = sampleapp:main
      [console_scripts]
      initialize_sampleapp_db = sampleapp.scripts.initializedb:main
      """,
      )

