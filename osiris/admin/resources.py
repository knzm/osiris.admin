# -*- coding: utf-8 -*-

from zope.interface import implementer, provider

from sqlalchemy import exceptions as sqlalchemy_exceptions

from pyramid.interfaces import IRequest
from pyramid.exceptions import NotFound
from pyramid.security import Allow, Authenticated, ALL_PERMISSIONS
from pyramid_formalchemy import actions

from osiris.admin import model_config
from osiris.admin.interface import (
    IAdminItemContext,
    IAdminListContext,
    IAdminRootContext,
    IAdminRootContextFactory,
    IAdminListContextFactory,
    IAdminItemContextFactory,
    IModel,
    IModelConfig,
    )
from osiris.admin.utils import get_model_config
from osiris.auth import get_current_user

__all__ = ['AdminItemContext', 'AdminListContext', 'AdminContext']


def fa_url(request, *args, **kwargs):
    matchdict = request.matchdict.copy()
    if 'traverse' in matchdict:
        del matchdict['traverse']
    if kwargs:
        matchdict['_query'] = kwargs
    return request.route_url(
        request.route_name,
        traverse=tuple(map(str, args)),
        **matchdict)


@provider(IAdminRootContextFactory)
@implementer(IAdminRootContext)
class AdminRootContext(object):
    __acl__ = [
        (Allow, Authenticated, 'view'),
        (Allow, 'admin', ALL_PERMISSIONS),
        # (Allow, 'editor', ('view', 'new', 'edit', 'delete')),
        ]

    def __init__(self, request):
        self.request = request
        self.__parent__ = None
        self.title = 'Admin'

        if self.__admin_menu__:
            admin_menu = self.__admin_menu__
        else:
            models = request.registry.getUtilitiesFor(IModel)
            admin_menu = sorted([name for name, ob in models])
        admin_menu = [
            get_model_config(self.request, name)
            for name in admin_menu]

        request.route_name = self.__fa_route_name__
        request.session_factory = self.__session_factory__
        request.query_factory = self.__query_factory__
        request.fa_url = self.fa_url
        request.model_instance = None
        request.model_class = None
        request.model_name = None
        request.model_id = None
        request.relation = None
        request.format = 'html'
        request.admin_menu = admin_menu

        request.current_user = get_current_user(self.request)

        request.actions = actions.RequestActions()

        langs = request.registry.settings.get('available_languages', '')
        if langs:
            if isinstance(langs, basestring):
                langs = langs.split()
            request.actions['languages'] = actions.Languages(*langs)

        themes = request.registry.settings.get('available_themes', '')
        if themes:
            if isinstance(themes, basestring):
                themes = themes.split()
            request.actions['themes'] = actions.Themes(*themes)

    def fa_url(self, *args, **kwargs):
        return fa_url(self.request, *args, **kwargs)

    def __getitem__(self, item):
        model_class = self.request.registry.queryUtility(IModel, name=item)
        if model_class is None:
            raise KeyError()

        registry = self.request.registry
        factory = registry.getUtility(IAdminListContextFactory)
        context = factory(self.request, name=item, parent=self)

        return context


@provider(IAdminListContextFactory)
@implementer(IAdminListContext)
class AdminListContext(object):

    def __init__(self, request, name, parent):
        self.request = request
        self.__name__ = name
        self.__parent__ = parent

        model_class = self.request.registry.queryUtility(IModel, name=name)
        assert model_class

        config = get_model_config(self.request, name)
        self.title = config.get("title", name)

        self.request.model_name = name
        self.request.model_class = model_class

    def fa_url(self, *args, **kwargs):
        return fa_url(self.request, *args[1:], **kwargs)

    def __getitem__(self, item):
        model_class = self.request.model_class
        assert model_class is not None

        name = self.request.path.split('/')[-1] #view name
        if name == item:
            name = ''

        registry = self.request.registry
        factory = registry.getUtility(IAdminItemContextFactory)
        context = factory(self.request, name=item, parent=self)

        return context


@provider(IAdminItemContextFactory)
@implementer(IAdminItemContext)
class AdminItemContext(object):

    def __init__(self, request, name, parent):
        self.request = request
        self.__name__ = name
        self.__parent__ = parent

        # request.model_class and request.model_name are already set
        model_class = request.model_class
        assert model_class is not None

        config = get_model_config(self.request, request.model_name)
        self.title = config.get("title", request.model_name)

        instance = self.prepare_instance(name)
        if instance is None:
            raise KeyError()

        self.request.model_id = name
        self.request.model_instance = instance

    def prepare_instance(self, name):
        request = self.request
        query = request.session_factory.query(request.model_class)
        try:
            model_instance = request.query_factory(request, query, id=name)
        except sqlalchemy_exceptions.SQLAlchemyError, exc:
            log.exception(exc)
            request.session_factory().rollback()
            return None

        return model_instance

    def fa_url(self, *args, **kwargs):
        return fa_url(self.request, *args[2:], **kwargs)


def includeme(config):
    config.registry.registerUtility(AdminRootContext, IAdminRootContextFactory)
    config.registry.registerUtility(AdminListContext, IAdminListContextFactory)
    config.registry.registerUtility(AdminItemContext, IAdminItemContextFactory)
