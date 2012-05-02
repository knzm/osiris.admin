# -*- coding: utf-8 -*-

__all__ = [
    'model_config',
    'get_model_config',
]

class model_config(object):
    def __init__(self, title):
        self.title = title

    def __call__(self, wrapped):
        settings = self.__dict__.copy()
        wrapped.__osiris_model_config__ = settings
        return wrapped


def get_model_config(wrapped):
    return getattr(wrapped, "__osiris_model_config__", {})


def includeme(config):
    config.add_directive('osiris_admin', 'osiris.admin.directive.osiris_admin')
    config.add_directive('osiris_admin_routing', 'osiris.admin.routing.setup')
    config.include('osiris.admin.resources')
    config.include('osiris.admin.views')
    config.include('osiris.admin.forms')
