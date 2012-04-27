# -*- coding: utf-8 -*-

from zope.interface import Interface, Attribute

__all__ = [
    'IModelViewFactory',
    'IModelGrid',
    'IModelForm',
    'IModelAddForm',
    'IModelEditForm',
    'IModelViewForm',
    'IModelType',
    'INewsModelType',
    ]


class IModelViewFactory(Interface):
    def getModelIndexView(self): pass
    def getModelListView(self): pass
    def getModelItemView(self): pass


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
    def bind(self, instances, session=None, data=None, request=None): pass
    def render(self, **kw): pass


class IModelForm(Interface):
    def bind(self, model=None, session=None, data=None, request=None): pass
    def validate(self): pass
    def sync(self): pass
    def render(self, **kw): pass
    errors = Attribute("Errors")
    model = Attribute("Model")


class IModelAddForm(IModelForm):
    pass


class IModelEditForm(IModelForm):
    pass


class IModelViewForm(IModelForm):
    pass


class IModelType(Interface):
    pass


class INewsModelType(IModelType):
    pass
