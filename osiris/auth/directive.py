# -*- coding: utf-8 -*-

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from osiris.admin.utils import guess_dbsession
from .security import groupfinder
from .views import AccountView


def osiris_auth(config, settings_prefix="osiris.auth.",
                url_prefix="account",
                session_factory=None,
                account_view_handler=None):
    secret = config.registry.settings.get(settings_prefix+"secret")
    authn_policy = AuthTktAuthenticationPolicy(
        secret, callback=groupfinder)
    config.set_authentication_policy(authn_policy)

    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)

    if not session_factory:
        session_factory = guess_dbsession(config)

    class RootContext(object):
        def __init__(self, request):
            request.session_factory = session_factory

    if account_view_handler is None:
        account_view_handler = AccountView

    config.add_route('login', url_prefix+'/login', factory=RootContext)
    config.add_route('logout', url_prefix+'/logout')

    config.add_forbidden_view(
        view=account_view_handler, attr='login_form',
        renderer='osiris.auth:templates/login.mak')

    # GET /account/login
    config.add_view(route_name="login",
                    request_method='GET',
                    view=account_view_handler, attr='login_form',
                    renderer='osiris.auth:templates/login.mak')


    # POST /account/login
    config.add_view(route_name="login",
                    request_method='POST',
                    view=account_view_handler, attr='login',
                    renderer='osiris.auth:templates/login.mak')

    # GET /account/logout
    # POST /account/logout
    config.add_view(route_name="logout",
                    # name='',
                    view=account_view_handler, attr='logout')


