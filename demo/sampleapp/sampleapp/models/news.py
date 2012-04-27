# -*- coding: utf-8 -*-

from sqlalchemy import UnicodeText, Integer
from formalchemy import Column

from zope.interface import directlyProvides

from osiris.admin.interface import INewsModelType
from sampleapp.models.base import BaseModel

__all__ = ['NewsModel']


class NewsModel(BaseModel):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, label='ID')
    title = Column(UnicodeText, nullable=False, label=u"タイトル")
    body = Column(UnicodeText, default="", label=u"本文")

directlyProvides(NewsModel, INewsModelType)
