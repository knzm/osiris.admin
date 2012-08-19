# -*- coding: utf-8 -*-

from zope.interface import implementer
from zope.component import adapter

from formalchemy.fields import TextAreaFieldRenderer

from osiris.admin.interface import (
    IModelGrid,
    IModelAddForm,
    IModelEditForm,
    IModelViewForm,
    IModel,
    )

from osiris.admin.forms import GenericModelForm, GenericModelGrid

from sampleapp.models import NewsModel


@adapter(NewsModel)
class NewsModelGrid(GenericModelGrid):
    def update_grid(self, grid):
        super(NewsModelGrid, self).update_grid(grid)


@adapter(NewsModel)
class NewsModelForm(GenericModelForm):

    def get_form(self, model_class):
        form = super(NewsModelForm, self).get_form(model_class)
        form["body"].set(renderer=TextAreaFieldRenderer)
        return form


def includeme(config):
    config.registry.registerAdapter(NewsModelGrid, provided=IModelGrid)
    config.registry.registerAdapter(NewsModelForm, provided=IModelAddForm)
    config.registry.registerAdapter(NewsModelForm, provided=IModelEditForm)
