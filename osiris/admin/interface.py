# -*- coding: utf-8 -*-

from zope.interface import Interface, Attribute

__all__ = [
    'IAdminModelConfig',
    'IAdminRootContext',
    'IAdminListContext',
    'IAdminItemContext',
    'IAdminRootContextFactory',
    'IAdminListContextFactory',
    'IAdminItemContextFactory',
    'IModelIndexViewFactory',
    'IModelListViewFactory',
    'IModelItemViewFactory',
    'IModelGrid',
    'IModelForm',
    'IModelAddForm',
    'IModelEditForm',
    'IModelViewForm',
    'IModel',
    'IModelConfig',
    ]


class IAdminContext(Interface):
    request = Attribute("Request")
    __parent__ = Attribute("Parent")

    def fa_url(self, *args, **kwargs):
        pass


class IAdminRootContext(IAdminContext):
    __fa_route_name__ = Attribute("fa_route_name")
    __models__ = Attribute("Models")
    __forms__ = Attribute("Forms")
    __session_factory__ = Attribute("session_factory")
    __query_factory__ = Attribute("query_factory")
    __model_class__ = Attribute("model_class")
    __admin_menu__ = Attribute("admin_menu")


class IAdminListContext(IAdminContext):
    pass


class IAdminItemContext(IAdminContext):
    pass


class IAdminRootContextFactory(Interface):
    def __call__(self, **kw):
        pass


class IAdminListContextFactory(Interface):
    def __call__(self, **kw):
        pass


class IAdminItemContextFactory(Interface):
    def __call__(self, **kw):
        pass


class IModelIndexViewFactory(Interface):
    def __call__(self, **kw):
        pass


class IModelListViewFactory(Interface):
    def __call__(self, **kw):
        pass


class IModelItemViewFactory(Interface):
    def __call__(self, **kw):
        pass


class IModelIndexView(Interface):
    def index(self, **kwargs): pass


class IModelListView(Interface):
    def index(self, **kwargs): pass


class IModelItemView(Interface):
    def show(self): pass
    def new(self): pass
    def create(self): pass
    def edit(self): pass
    def update(self): pass
    def delete(self): pass


class IModelIndexViewFactory(Interface):
    def get_view(self): pass


class IModelListViewFactory(Interface):
    def get_view(self): pass


class IModelItemViewFactory(Interface):
    def get_view(self): pass


class IModelGrid(Interface):
    def __call__(self, request): pass
    def bind(self, instances, session=None, data=None): pass
    def render(self, **kw): pass
    engine = Attribute("Engine")


class IModelForm(Interface):
    def __call__(self, request): pass
    def bind(self, model=None, session=None, data=None): pass
    def validate(self): pass
    def sync(self): pass
    def render(self, **kw): pass
    errors = Attribute("Errors")
    model = Attribute("Model")
    engine = Attribute("Engine")


class IModelAddForm(IModelForm):
    pass


class IModelEditForm(IModelForm):
    pass


class IModelViewForm(IModelForm):
    pass


class IModel(Interface):
    pass


class IModelConfig(Interface):
    pass
