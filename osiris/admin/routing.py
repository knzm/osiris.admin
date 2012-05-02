# -*- coding: utf-8 -*-

from pyramid import httpexceptions as exc

from .interface import (
    IModelIndexViewFactory,
    IModelListViewFactory,
    IModelItemViewFactory,
    IAdminRootContext,
    IAdminListContext,
    IAdminItemContext,
    )

def setup(config, root_factory):

    ModelIndexView = config.registry.getUtility(IModelIndexViewFactory)
    ModelListView = config.registry.getUtility(IModelListViewFactory)
    ModelItemView = config.registry.getUtility(IModelItemViewFactory)

    config.add_route('admin_redirect', 'admin')
    config.add_route('admin', 'admin/*traverse', factory=root_factory)

    def redirect(request):
        """redirect /{route_name} to /{route_name}/"""
        matchdict = request.matchdict
        url = request.route_url('admin', traverse=(), **matchdict)
        return exc.HTTPFound(location=url)

    config.add_view(redirect, route_name='admin_redirect')

    # GET /admin
    config.add_view(route_name="admin",
                    context=IAdminRootContext,
                    request_method='GET',
                    permission='view',
                    view=ModelIndexView, attr='index',
                    renderer='osiris.admin:templates/admin/models.mak')

    # GET /admin/{model}
    config.add_view(route_name="admin",
                    context=IAdminListContext,
                    request_method='GET',
                    permission='view',
                    view=ModelListView, attr='index',
                    renderer='osiris.admin:templates/admin/listing.mak')

    # GET /admin/{model}/new
    config.add_view(route_name="admin",
                    context=IAdminListContext,
                    name='new',
                    request_method='GET',
                    permission='new',
                    view=ModelItemView, attr='new',
                    renderer='osiris.admin:templates/admin/new.mak')

    # POST /admin/{model}
    config.add_view(route_name="admin",
                    context=IAdminListContext,
                    request_method='POST',
                    permission='new',
                    view=ModelItemView, attr='create',
                    renderer='osiris.admin:templates/admin/new.mak')

    # GET /admin/{model}/{id}
    config.add_view(route_name="admin",
                    context=IAdminItemContext, name='',
                    request_method='GET',
                    permission='view',
                    view=ModelItemView, attr='show',
                    renderer='osiris.admin:templates/admin/show.mak')

    # GET /admin/{model}/{id}/edit
    config.add_view(route_name="admin",
                    context=IAdminItemContext, name='edit',
                    request_method='GET',
                    permission='edit',
                    view=ModelItemView, attr='edit',
                    renderer='osiris.admin:templates/admin/edit.mak')

    # POST /admin/{model}/{id}/edit
    config.add_view(route_name="admin",
                    context=IAdminItemContext, name='edit',
                    request_method='POST',
                    permission='edit',
                    view=ModelItemView, attr='update',
                    renderer='osiris.admin:templates/admin/edit.mak')

    # POST /admin/{model}/{id}
    config.add_view(route_name="admin",
                    context=IAdminItemContext, name='',
                    request_method='POST',
                    permission='edit',
                    view=ModelItemView, attr='update',
                    renderer='json')

    # POST /admin/{model}/{id}/delete
    config.add_view(route_name="admin",
                    context=IAdminItemContext, name='delete',
                    request_method='POST',
                    permission='delete',
                    view=ModelItemView, attr='delete',
                    renderer='osiris.admin:templates/admin/edit.mak')

    # DELETE /admin/{model}/{id}
    config.add_view(route_name="admin",
                    context=IAdminItemContext, name='',
                    request_method='DELETE',
                    permission='delete',
                    view=ModelItemView, attr='delete',
                    renderer='osiris.admin:templates/admin/edit.mak')
