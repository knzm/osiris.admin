# -*- coding: utf-8 -*-

from sqlalchemy import exceptions as sqlalchemy_exceptions
from pyramid_formalchemy import actions
from pyramid.exceptions import NotFound

__all__ = ['AdminItemContext', 'AdminListContext', 'AdminContext']


def get_model(request):
    if request.model_class:
        return request.model_class
    model_name = request.model_name
    model_class = None
    if isinstance(request.models, list):
        for model in request.models:
            if model.__name__ == model_name:
                model_class = model
                break
    elif hasattr(request.models, model_name):
        model_class = getattr(request.models, model_name)
    if model_class is None:
        raise NotFound(request.path)
    request.model_class = model_class
    return model_class


class BaseAdminContext(object):
    def __init__(self, request, name):
        self.__name__ = name
        self.__parent__ = None
        self.request = request

        if hasattr(self, '__fa_route_name__'):
            request.route_name = self.__fa_route_name__
            request.models = self.__models__
            request.forms = self.__forms__
            request.session_factory = self.__session_factory__
            request.query_factory = self.__query_factory__
            request.fa_url = self.fa_url
            request.model_instance = None
            request.model_class = None
            request.model_name = None
            request.model_id = None
            request.relation = None
            request.format = 'html'
            if self.__model_class__:
                request.model_class = self.__model_class__
                request.model_name = self.__model_class__.__name__
            request.admin_menu = self.__admin_menu__

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

    def _fa_url(self, *args, **kwargs):
        matchdict = self.request.matchdict.copy()
        if 'traverse' in matchdict:
            del matchdict['traverse']
        if kwargs:
            matchdict['_query'] = kwargs
        return self.request.route_url(
            self.__fa_route_name__,
            traverse=tuple([str(a) for a in args]),
            **matchdict)


class AdminItemContext(BaseAdminContext):

    def __init__(self, request, name):
        BaseAdminContext.__init__(self, request, name)
        query = request.session_factory.query(request.model_class)
        try:
            request.model_instance = request.query_factory(
                request, query, id=name)
        except sqlalchemy_exceptions.SQLAlchemyError, exc:
            log.exception(exc)
            request.session_factory().rollback()
            raise NotFound(request.path)

        if request.model_instance is None:
            raise NotFound(request.path)
        request.model_id = name

    def fa_url(self, *args, **kwargs):
        return self._fa_url(*args[2:], **kwargs)


class AdminListContext(BaseAdminContext):

    def __init__(self, request, name=None):
        BaseAdminContext.__init__(self, request, name)
        if name is None:
            # request.model_class and request.model_name are already set
            model = request.model_class
        else:
            request.model_name = name
            model = get_model(self.request)
        if hasattr(model, '__acl__'):
            # get permissions from SA class
            self.__acl__ = model.__acl__

    def fa_url(self, *args, **kwargs):
        return self._fa_url(*args[1:], **kwargs)

    def get_model(self):
        return get_model(self.request)

    def __getitem__(self, item):
        name = self.request.path.split('/')[-1] #view name
        if name == item:
            name = ''

        mixin_name = '%sCustom%s_%s_%s_%s' % (
            self.request.model_class.__name__, AdminItemContext.__name__,
            self.request.route_name, name, self.request.method)
        mixin = type(str(mixin_name), (AdminItemContext,), {})
        factory = self.request.registry.pyramid_formalchemy_views.get(
            mixin.__name__, mixin)
        try:
            model = factory(self.request, item)
        except NotFound:
            raise KeyError()
        model.__parent__ = self

        return model


class AdminRootContext(BaseAdminContext):

    def __init__(self, request):
        BaseAdminContext.__init__(self, request, None)

    def fa_url(self, *args, **kwargs):
        return self._fa_url(*args, **kwargs)

    def __getitem__(self, item):
        self.request.model_name = item.title() + "Model"
        model_class = get_model(self.request)
        mixin_name = '%sCustom%s_%s__%s' % (
            model_class.__name__, AdminListContext.__name__,
            self.request.route_name, self.request.method)
        mixin = type(mixin_name, (AdminListContext,), {})
        factory = self.request.registry.pyramid_formalchemy_views.get(
            mixin.__name__, mixin)
        model = factory(self.request, item)
        model.__parent__ = self
        if hasattr(model, '__acl__'):
            # propagate permissions to parent
            self.__acl__ = model.__acl__

        return model
