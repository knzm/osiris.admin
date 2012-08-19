import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'osiris.admin',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'pyramid_tm',
    'pyramid_jinja2',
    'mako',
    'pyramid_debugtoolbar',
    'pyramid_tw2',
    'waitress',
    ]

dependency_links = [
    "https://github.com/knzm/pyramid_tw2/tarball/master#egg=pyramid_tw2-1.0.0dev",
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
      dependency_links=dependency_links,
      entry_points="""\
      [paste.app_factory]
      main = sampleapp:main
      [console_scripts]
      initialize_sampleapp_db = sampleapp.scripts.initializedb:main
      """,
      )

