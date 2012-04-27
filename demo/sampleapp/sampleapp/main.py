# -*- coding: utf-8 -*-

from pyramid.config import Configurator
from .resources import RootContext

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=RootContext)
    config.include('osiris.admin')
    config.include('osiris.admin.views')
    config.include('osiris.admin.forms')
    config.osiris_admin(package='sampleapp', admin_menu=[
            'news',
            ])
    config.include('.models')
    config.include('.routing')
    config.include('.i18n')

    return config.make_wsgi_app()

