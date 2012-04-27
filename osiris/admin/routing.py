# -*- coding: utf-8 -*-

from .interface import (
    IModelViewFactory,
    )

from .resources import (
    AdminRootContext,
    AdminListContext,
    AdminItemContext,
    )


def osiris_admin(config, route_name="admin", admin_menu=None,
                 package=None, models=None, forms=None,
                 session_factory=None, query_factory=None):
    config.include('pyramid_formalchemy')

    try:
        # Add fanstatic tween if available
        config.include('pyramid_fanstatic')
    except ImportError:
        log.warn('You should install pyramid_fanstatic or register a fanstatic'
                 ' middleware by hand')

    if models:
        models = config.maybe_dotted(models)
    if forms:
        forms = config.maybe_dotted(forms)
    if session_factory:
        session_factory = config.maybe_dotted(session_factory)

    if package:
        if not models:
            models = config.maybe_dotted('%s.models' % package)
        if not forms:
            forms = config.maybe_dotted('%s.forms' % package)
        if not session_factory and models:
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

    view_factory = config.registry.getUtility(IModelViewFactory)
    ModelIndexView = view_factory.getModelIndexView()
    ModelListView = view_factory.getModelListView()
    ModelItemView = view_factory.getModelItemView()

    class AdminContext(AdminRootContext):
        __fa_route_name__ = route_name
        __forms__ = forms
        __models__ = models
        __model_class__ = None
        __session_factory__ = session_factory
        __query_factory__ = staticmethod(query_factory)
        __admin_menu__ = admin_menu or []

    config.add_route('admin_redirect', 'admin')
    config.add_route('admin', 'admin/*traverse', factory=AdminContext)

    def redirect(request):
        """redirect /{route_name} to /{route_name}/"""
        matchdict = request.matchdict
        url = request.route_url('admin', traverse=(), **matchdict)
        return HTTPFound(location=url)

    config.add_view(redirect, route_name='admin_redirect')

    template_package = 'osiris.admin'

    # GET /admin
    config.add_view(route_name="admin",
                    context=AdminContext,
                    request_method='GET',
                    permission='view',
                    view=ModelIndexView, attr='index',
                    renderer='%s:templates/admin/models.mak' % template_package)

    # GET /admin/{model}
    config.add_view(route_name="admin",
                    context=AdminListContext,
                    request_method='GET',
                    permission='view',
                    view=ModelListView, attr='index',
                    renderer='%s:templates/admin/listing.mak' % template_package)

    # GET /admin/{model}/new
    config.add_view(route_name="admin",
                    context=AdminListContext,
                    name='new',
                    request_method='GET',
                    permission='new',
                    view=ModelItemView, attr='new',
                    renderer='%s:templates/admin/new.mak' % template_package)

    # POST /admin/{model}
    config.add_view(route_name="admin",
                    context=AdminListContext,
                    request_method='POST',
                    permission='new',
                    view=ModelItemView, attr='create',
                    renderer='%s:templates/admin/new.mak' % template_package)

    # GET /admin/{model}/{id}
    config.add_view(route_name="admin",
                    context=AdminItemContext, name='',
                    request_method='GET',
                    permission='view',
                    view=ModelItemView, attr='show',
                    renderer='%s:templates/admin/show.mak' % template_package)

    # GET /admin/{model}/{id}/edit
    config.add_view(route_name="admin",
                    context=AdminItemContext, name='edit',
                    request_method='GET',
                    permission='edit',
                    view=ModelItemView, attr='edit',
                    renderer='%s:templates/admin/edit.mak' % template_package)

    # POST /admin/{model}/{id}/edit
    config.add_view(route_name="admin",
                    context=AdminItemContext, name='edit',
                    request_method='POST',
                    permission='edit',
                    view=ModelItemView, attr='update',
                    renderer='%s:templates/admin/edit.mak' % template_package)

    # POST /admin/{model}/{id}
    config.add_view(route_name="admin",
                    context=AdminItemContext, name='',
                    request_method='POST',
                    permission='edit',
                    view=ModelItemView, attr='update',
                    renderer='json')

    # POST /admin/{model}/{id}/delete
    config.add_view(route_name="admin",
                    context=AdminItemContext, name='delete',
                    request_method='POST',
                    permission='delete',
                    view=ModelItemView, attr='delete',
                    renderer='%s:templates/admin/edit.mak' % template_package)

    # DELETE /admin/{model}/{id}
    config.add_view(route_name="admin",
                    context=AdminItemContext, name='',
                    request_method='DELETE',
                    permission='delete',
                    view=ModelItemView, attr='delete',
                    renderer='%s:templates/admin/edit.mak' % template_package)
