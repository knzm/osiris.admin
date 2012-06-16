# -*- coding: utf-8 -*-

import venusian

__all__ = [
    'model_config',
    'get_model_config',
]

class model_config(object):
    venusian = venusian

    def __init__(self, name='', title=''):
        self.name = name
        self.title = title

    def __call__(self, wrapped):
        settings = self.__dict__.copy()

        if not settings["name"]:
            settings["name"] = wrapped.__name__

        if not settings["title"]:
            settings["title"] = wrapped.__name__

        def callback(context, name, ob):
            config = context.config.with_package(info.module)
            config.add_model(model=ob, **settings)

        info = self.venusian.attach(wrapped, callback, category='pyramid')

        return wrapped


def get_model_config(request, name):
    from osiris.admin.interface import IModelConfig
    return request.registry.getUtility(IModelConfig, name=name)


def includeme(config):
    config.add_directive('osiris_admin', 'osiris.admin.directive.osiris_admin')
    config.add_directive('add_model', 'osiris.admin.directive.add_model')
    config.add_directive('osiris_admin_routing', 'osiris.admin.routing.setup')
    config.include('osiris.admin.resources')
    config.include('osiris.admin.views')
    config.include('osiris.admin.forms')
