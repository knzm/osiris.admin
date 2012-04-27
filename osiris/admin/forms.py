# -*- coding: utf-8 -*-

from pyramid.threadlocal import get_current_request

from sqlalchemy.orm.scoping import ScopedSession
from formalchemy import forms
from formalchemy import tables
from pyramid_formalchemy.utils import TemplateEngine

from zope.interface import implements
from zope.component import adapts

from osiris.admin.interface import (
    IModelGrid,
    IModelAddForm,
    IModelEditForm,
    IModelViewForm,
    IModelType,
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


class GenericModelGrid(object):
    implements(IModelGrid)
    adapts(IModelType)

    grid_class = tables.Grid

    def __init__(self, model_class):
        self.model_class = model_class
        self.grid = self.grid_class(self.model_class)

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
        try:
            grid.edit
        except AttributeError:
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
            grid.readonly = True

    def render(self, **kw):
        return self.grid.render(**kw)


class GenericModelForm(object):
    implements(IModelAddForm, IModelEditForm)
    adapts(IModelType)

    fieldset_class = forms.FieldSet

    def __init__(self, model_class):
        self.model_class = model_class
        self.form = self.fieldset_class(self.model_class)

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


class ModelViewForm(GenericModelForm):
    implements(IModelViewForm)

    def __init__(self, model_class):
        super(ModelViewForm, self).__init__(model_class)
        self.form.readonly = True


def includeme(config):
    config.registry.registerAdapter(GenericModelGrid, provided=IModelGrid)
    config.registry.registerAdapter(GenericModelForm, provided=IModelAddForm)
    config.registry.registerAdapter(GenericModelForm, provided=IModelEditForm)
    config.registry.registerAdapter(ModelViewForm, provided=IModelViewForm)
