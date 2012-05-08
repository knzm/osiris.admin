# -*- coding: utf-8 -*-

from collections import OrderedDict

from pyramid.interfaces import IBeforeRender

from .resources import AdminRootContext


def AdminRootContextFactory(route_name,
                            session_factory, query_factory,
                            admin_menu):
    class AdminContext(AdminRootContext):
        __fa_route_name__ = route_name
        __session_factory__ = session_factory
        __query_factory__ = staticmethod(query_factory)
        __admin_menu__ = admin_menu
    return AdminContext


def osiris_admin(config, route_name="admin", admin_menu=None,
                 package=None, session_factory=None, query_factory=None,
                 root_factory=None):
    # config.include('pyramid_formalchemy')
    config.include('pyramid_fanstatic')
    config.include('fa.jquery')
    # config.include('fa.bootstrap')

    # from js.bootstrap import bootstrap
    from fa.bootstrap.fanstatic_resources import bootstrap
    def subscriber(event):
        bootstrap.need()
    config.add_subscriber(subscriber, IBeforeRender)

    config.override_asset(
        to_override="pyramid_formalchemy:templates/forms/",
        override_with="fa.bootstrap:templates/forms/")

    if root_factory:
        config.osiris_admin_routing(root_factory)
        return

    if session_factory:
        session_factory = config.maybe_dotted(session_factory)

    if package and not session_factory:
        try:
            models = config.maybe_dotted('%s.models' % package)
        except ValueError:
            pass
        else:
            # alchemy
            session_factory = getattr(models, "DBSession", None)
            if not session_factory:
                # Akhet
                session_factory = getattr(models, "Session", None)

    if not query_factory:
        def query_factory(request, query, id=None):
            if id is not None:
                return query.get(id)
            else:
                return query

    admin_menu = OrderedDict([
            (key, config.maybe_dotted(val))
            for key, val in admin_menu or ()])
    root_factory = AdminRootContextFactory(
        route_name=route_name,
        session_factory=session_factory,
        query_factory=query_factory,
        admin_menu=admin_menu)

    config.osiris_admin_routing(root_factory)
