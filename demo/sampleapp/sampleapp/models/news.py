# -*- coding: utf-8 -*-

from sqlalchemy import UnicodeText, Integer
from formalchemy import Column

from zope.interface import provider

from osiris.admin import model_config

from sampleapp.interface import INewsModel
from sampleapp.models.base import BaseModel

__all__ = ['NewsModel']


@provider(INewsModel)
@model_config(name='news', title=u"新着記事")
class NewsModel(BaseModel):

    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, label='ID')
    title = Column(UnicodeText, nullable=False, label=u"タイトル")
    body = Column(UnicodeText, default="", label=u"本文")
