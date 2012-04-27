# -*- coding: utf-8 -*-

def static_routes(config):
    config.add_static_view('static', 'static', cache_max_age=3600)


def error_routes(config):
    config.scan('.views.error')


def includeme(config):
    config.include(static_routes)
    config.include(error_routes)
