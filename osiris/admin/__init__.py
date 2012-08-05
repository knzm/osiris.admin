# -*- coding: utf-8 -*-

import venusian

__all__ = [
    'model_config',
]


class model_config(object):
    venusian = venusian

    def __init__(self, name='', title='', provides=None):
        self.settings = {
            "name": name,
            "title": title,
            "provides": provides,
            }

    def register(self, scanner, name, wrapped):
        settings = self.settings.copy()
        if not settings["name"]:
            settings["name"] = wrapped.__name__
        if not settings["title"]:
            settings["title"] = wrapped.__name__
        config = scanner.config.with_package(self.info.module)
        config.add_model(model=wrapped, **settings)

    def __call__(self, wrapped):
        self.info = self.venusian.attach(wrapped, self.register)
        return wrapped


def includeme(config):
    config.add_directive('osiris_admin', 'osiris.admin.directive.osiris_admin')
    config.add_directive('add_model', 'osiris.admin.directive.add_model')
    config.add_directive('osiris_admin_routing', 'osiris.admin.routing.setup')
    config.include('osiris.admin.resources')
    config.include('osiris.admin.views')
    config.include('osiris.admin.forms')
    config.include('osiris.auth')
