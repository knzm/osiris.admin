# -*- coding: utf-8 -*-

from zope.interface import implementer
from zope.component import adapter

from pyramid.threadlocal import get_current_request

from sqlalchemy.orm.scoping import ScopedSession

from formalchemy import forms
from formalchemy import tables

from osiris.admin.interface import (
    IModelGrid,
    IModelAddForm,
    IModelEditForm,
    IModelViewForm,
    IModel,
    )

__all__ = [
    'GenericModelGrid',
    'GenericModelForm',
    'ModelViewForm',
]

EDIT_LINK_TEMPLATE = '''\
<form action="%(url)s" method="GET" class="ui-grid-icon ui-widget-header ui-corner-all">
<input type="submit" class="ui-grid-icon ui-icon ui-icon-pencil" title="%(label)s" value="%(label)s" />
</form>
'''

DELETE_LINK_TEMPLATE = '''\
<form action="%(url)s" method="POST" class="ui-grid-icon ui-state-error ui-corner-all">
<input type="submit" class="ui-icon ui-icon-circle-close" title="%(label)s" value="%(label)s" />
</form>
'''


@implementer(IModelGrid)
@adapter(IModel)
class GenericModelGrid(object):

    grid_class = tables.Grid

    def __init__(self, model_class):
        self.model_class = model_class
        self.grid = self.grid_class(self.model_class)
        self.grid.configure(pk=1)

    def bind(self, instances, session=None, data=None, request=None):
        if isinstance(session, ScopedSession):
            session = session.registry()
        self.grid = self.grid.bind(instances, session=session,
                                   data=data, request=request)
        self.grid.readonly = True
        self.update_grid(self.grid)

    def update_grid(self, grid):
        """Add edit and delete buttons to ``Grid``"""
        from formalchemy.i18n import get_translator
        from formalchemy.fields import Field, _pk
        from formalchemy import fatypes

        if not hasattr(grid, 'edit'):
            request = get_current_request()
            translator = get_translator(request=request)
            def edit_link(item):
                url = request.fa_url(
                    request.model_name, _pk(item), 'edit')
                return EDIT_LINK_TEMPLATE % dict(
                    url=url, label=translator('edit'))
            def delete_link(item):
                url = request.fa_url(
                    request.model_name, _pk(item), 'delete')
                return DELETE_LINK_TEMPLATE % dict(
                    url=url, label=translator('delete'))
            grid.append(Field('edit', fatypes.String, edit_link))
            grid.append(Field('delete', fatypes.String, delete_link))

        from formalchemy import fatypes
        from fa.jquery import utils
        from fa.jquery.renderers import ellipsys

        # metadatas = ('width', 'align', 'fixed', 'search', 'stype', 'searchoptions')
        for field in grid.render_fields.values():
            metadata = dict(search=0, sortable=1, id=field.key, name=field.key)
            searchoptions = dict(sopt=['eq', 'cn'])
            if field.is_relation:
                metadata.update(width=100, sortable=0)
            elif isinstance(field.type, (utils.Color, utils.Slider)):
                metadata.update(width=50, align='center')
            elif isinstance(field.type, fatypes.Text):
                field.set(renderer=ellipsys(field.renderer))
                metadata.update(search=1)
            elif isinstance(field.type, (fatypes.String, fatypes.Unicode)):
                metadata.update(search=1)
            elif isinstance(field.type, (fatypes.Date, fatypes.Integer)):
                metadata.update(width=70, align='center')
            elif isinstance(field.type, fatypes.DateTime):
                metadata.update(width=120, align='center')
            elif isinstance(field.type, fatypes.Boolean):
                metadata.update(width=30, align='center')
            if metadata['search']:
                metadata['searchoptions'] = searchoptions
            # metadata = dict(json=dumps(metadata))
            # metadata['label'] = dumps(field.label())
            field.set(metadata=metadata)

    def render(self, **kw):
        return self.grid.render(**kw)

    # def engine():
    #     def fget(self):
    #         return self.grid.engine
    #     def fset(self, engine):
    #         self.grid.engine = engine
    #     return locals()
    # engine = property(**engine())


@implementer(IModelAddForm, IModelEditForm)
@adapter(IModel)
class GenericModelForm(object):

    fieldset_class = forms.FieldSet

    def __init__(self, model_class):
        self.model_class = model_class
        self.form = self.get_form(model_class)

    def get_form(self, model_class):
        return self.fieldset_class(self.model_class)

    def bind(self, model=None, session=None, data=None, request=None):
        if isinstance(session, ScopedSession):
            session = session.registry()
        self.form = self.form.bind(model=model, session=session,
                                   data=data, request=request)

    def validate(self):
        return self.form.validate()

    def sync(self):
        self.form.sync()

    def render(self, **kw):
        return self.form.render(**kw)

    @property
    def errors(self):
        return self.form.errors

    @property
    def model(self):
        return self.form.model

    # def engine():
    #     def fget(self):
    #         try:
    #             return self.form.engine
    #         except AttributeError:
    #             return None
    #     def fset(self, engine):
    #         self.form.engine = engine
    #     return locals()
    # engine = property(**engine())


@implementer(IModelViewForm)
class ModelViewForm(GenericModelForm):

    def __init__(self, model_class):
        super(ModelViewForm, self).__init__(model_class)
        self.form.readonly = True


def includeme(config):
    config.registry.registerAdapter(GenericModelGrid, provided=IModelGrid)
    config.registry.registerAdapter(GenericModelForm, provided=IModelAddForm)
    config.registry.registerAdapter(GenericModelForm, provided=IModelEditForm)
    config.registry.registerAdapter(ModelViewForm, provided=IModelViewForm)
