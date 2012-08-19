# -*- coding: utf-8 -*-

from zope.interface import implementer
from zope.component import adapter

from osiris.admin.interface import (
    IModelGrid,
    IModelAddForm,
    IModelEditForm,
    IModelViewForm,
    IModel,
    )

from formalchemy.fields import TextAreaFieldRenderer

from osiris.admin.forms import GenericModelForm

from sampleapp.interface import INewsModel


@implementer(IModelAddForm, IModelEditForm)
@adapter(INewsModel)
class NewsModelForm(GenericModelForm):

    def get_form(self, model_class):
        form = super(NewsModelForm, self).get_form(model_class)
        form["body"].set(renderer=TextAreaFieldRenderer)
        return form


def includeme(config):
    config.registry.registerAdapter(NewsModelForm, provided=IModelEditForm)
