# -*- coding: utf-8 -*-

from collections import OrderedDict

from zope.interface import directlyProvides
from pyramid.interfaces import IBeforeRender

from .interface import IModel, IModelConfig
from .resources import AdminRootContext
from .utils import guess_dbsession


def AdminRootContextFactory(route_name, session_factory, query_factory,
                            admin_menu):
    class AdminContext(AdminRootContext):
        __fa_route_name__ = route_name
        __session_factory__ = session_factory
        __query_factory__ = staticmethod(query_factory)
        __admin_menu__ = admin_menu
    return AdminContext


def osiris_admin(config, route_name="admin", url_prefix="admin",
                 session_factory=None, query_factory=None,
                 root_factory=None, admin_menu=None):
    config.include('pyramid_fanstatic')
    # config.include('pyramid_formalchemy')
    # config.include('fa.jquery')
    # config.include('fa.bootstrap')

    # from js.bootstrap import bootstrap
    # def subscriber(event):
    #     bootstrap.need()
    # config.add_subscriber(subscriber, IBeforeRender)

    config.override_asset(
        to_override="pyramid_formalchemy:templates/admin/",
        override_with="fa.jquery:templates/admin/")

    config.override_asset(
        to_override="pyramid_formalchemy:templates/forms/",
        override_with="fa.bootstrap:templates/forms/")

    if root_factory:
        config.osiris_admin_routing(root_factory)
        return

    if session_factory:
        session_factory = config.maybe_dotted(session_factory)

    if not session_factory:
        session_factory = guess_dbsession(config)

    if not query_factory:
        def query_factory(request, query, id=None):
            if id is not None:
                return query.get(id)
            else:
                return query

    root_factory = AdminRootContextFactory(
        route_name=route_name,
        session_factory=session_factory,
        query_factory=query_factory,
        admin_menu=admin_menu)

    config.osiris_admin_routing(root_factory, route_name, url_prefix)


def add_model(config, model, name, title=None, provides=IModel):
    settings = {
        'model': model,
        'name': name,
        'title': title,
        }
    if isinstance(provides, (tuple, list)):
        interfaces = provides
    else:
        interfaces = [provides]
    directlyProvides(model, *interfaces)
    config.registry.registerUtility(model, IModel, name=name)
    config.registry.registerUtility(settings, IModelConfig, name=name)
