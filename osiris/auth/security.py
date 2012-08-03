# -*- coding: utf-8 -*-

from pyramid.security import authenticated_userid

from .interface import IUserModel

__all__ = [
    'get_user_model', 'get_user', 'get_current_user',
    'authenticate', 'groupfinder',
]

def get_user_model(request):
    return request.registry.getUtility(IUserModel)


def get_user(request, username):
    return get_user_model(request).get_by_username(username)


def get_current_user(request):
    username = authenticated_userid(request)
    if username:
        return get_user(request, username)
    else:
        return None


def authenticate(username, password, request):
    user = get_user(request, username)
    return user.verify_password(password)


def groupfinder(username, request):
    user = get_user(request, username)
    return [group.group_name for group in user.groups]
