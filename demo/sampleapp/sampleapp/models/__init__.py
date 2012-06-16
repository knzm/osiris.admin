# -*- coding: utf-8 -*-

from base import *
# from news import *

def includeme(config):
    from sqlalchemy import engine_from_config
    engine = engine_from_config(config.registry.settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    # Find models and their configs
    config.scan(".")
