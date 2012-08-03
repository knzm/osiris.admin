# -*- coding: utf-8 -*-

from .security import get_current_user, authenticate

__all__ = [
    'get_current_user', 'authenticate',
]


def includeme(config):
    config.add_directive('osiris_auth', 'osiris.auth.directive.osiris_auth')
