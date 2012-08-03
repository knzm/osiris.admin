# -*- coding: utf-8 -*-

from pyramid.config import Configurator
from .resources import RootContext

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=RootContext)
    config.include('osiris.admin')
    config.osiris_admin()
    config.osiris_auth()
    config.include('.models')
    config.include('.forms')
    config.include('.routing')
    config.include('.i18n')

    # config.override_asset(
    #     to_override="osiris.admin:templates/admin/",
    #     override_with="sampleapp:templates/admin/")
    # config.override_asset(
    #     to_override="osiris.admin:templates/forms/",
    #     override_with="sampleapp:templates/forms/")

    return config.make_wsgi_app()

