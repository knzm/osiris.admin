# -*- coding: utf-8 -*-

from pyramid.i18n import TranslationStringFactory, get_localizer

tsf = TranslationStringFactory('sampleapp')

def add_localizer(event):
    request = event.request
    localizer = get_localizer(request)
    def translate(s):
        return localizer.translate(tsf(s))
    request.localizer = localizer
    request.translate = translate

def add_renderer_globals(event):
    request = event['request']
    if request:
        event['_'] = request.translate
    else:
        event['_'] = lambda s: s

def includeme(config):
    config.add_subscriber(add_localizer, 'pyramid.events.NewRequest')
    config.add_subscriber(add_renderer_globals, 'pyramid.events.BeforeRender')
