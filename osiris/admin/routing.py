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


def setup(config, root_factory, route_name, url_prefix):

    ModelIndexView = config.registry.getUtility(IModelIndexViewFactory)
    ModelListView = config.registry.getUtility(IModelListViewFactory)
    ModelItemView = config.registry.getUtility(IModelItemViewFactory)

    config.add_route(route_name+'_redirect', url_prefix)
    config.add_route(route_name, url_prefix+'/*traverse',
                     factory=root_factory)

    def redirect(request):
        """redirect /admin to /admin/"""
        matchdict = request.matchdict
        url = request.route_url('admin', traverse=(), **matchdict)
        return exc.HTTPFound(location=url)

    config.add_view(redirect, route_name=route_name+'_redirect')

    # GET /admin/
    config.add_view(route_name=route_name,
                    context=IAdminRootContext,
                    request_method='GET',
                    permission='view',
                    view=ModelIndexView, attr='index',
                    renderer='osiris.admin:templates/admin/models.mak')

    # GET /admin/{model}
    config.add_view(route_name=route_name,
                    context=IAdminListContext,
                    request_method='GET',
                    permission='view',
                    view=ModelListView, attr='index',
                    renderer='osiris.admin:templates/admin/listing.mak')

    # GET /admin/{model}/new
    config.add_view(route_name=route_name,
                    context=IAdminListContext,
                    name='new',
                    request_method='GET',
                    permission='new',
                    view=ModelItemView, attr='new',
                    renderer='osiris.admin:templates/admin/new.mak')

    # POST /admin/{model}
    config.add_view(route_name=route_name,
                    context=IAdminListContext,
                    request_method='POST',
                    permission='new',
                    view=ModelItemView, attr='create',
                    renderer='osiris.admin:templates/admin/new.mak')

    # GET /admin/{model}/{id}
    config.add_view(route_name=route_name,
                    context=IAdminItemContext, name='',
                    request_method='GET',
                    permission='view',
                    view=ModelItemView, attr='show',
                    renderer='osiris.admin:templates/admin/show.mak')

    # GET /admin/{model}/{id}/edit
    config.add_view(route_name=route_name,
                    context=IAdminItemContext, name='edit',
                    request_method='GET',
                    permission='edit',
                    view=ModelItemView, attr='edit',
                    renderer='osiris.admin:templates/admin/edit.mak')

    # POST /admin/{model}/{id}/edit
    config.add_view(route_name=route_name,
                    context=IAdminItemContext, name='edit',
                    request_method='POST',
                    permission='edit',
                    view=ModelItemView, attr='update',
                    renderer='osiris.admin:templates/admin/edit.mak')

    # POST /admin/{model}/{id}
    config.add_view(route_name=route_name,
                    context=IAdminItemContext, name='',
                    request_method='POST',
                    permission='edit',
                    view=ModelItemView, attr='update',
                    renderer='json')

    # POST /admin/{model}/{id}/delete
    config.add_view(route_name=route_name,
                    context=IAdminItemContext, name='delete',
                    request_method='POST',
                    permission='delete',
                    view=ModelItemView, attr='delete',
                    renderer='osiris.admin:templates/admin/edit.mak')

    # DELETE /admin/{model}/{id}
    config.add_view(route_name=route_name,
                    context=IAdminItemContext, name='',
                    request_method='DELETE',
                    permission='delete',
                    view=ModelItemView, attr='delete',
                    renderer='osiris.admin:templates/admin/edit.mak')
