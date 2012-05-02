# -*- coding: utf-8 -*-

from sqlalchemy import UnicodeText, Integer
from formalchemy import Column

from zope.interface import classProvides

from osiris.admin import model_config

from sampleapp.interface import INewsModelType
from sampleapp.models.base import BaseModel

__all__ = ['NewsModel']


@model_config(title=u"新着記事")
class NewsModel(BaseModel):
    classProvides(INewsModelType)

    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, label='ID')
    title = Column(UnicodeText, nullable=False, label=u"タイトル")
    body = Column(UnicodeText, default="", label=u"本文")
