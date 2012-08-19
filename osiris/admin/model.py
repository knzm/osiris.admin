# -*- coding: utf-8 -*-

import datetime
import re

from zope.interface import implementer

from sqlalchemy import Integer, Text, DateTime
from sqlalchemy import sql
from sqlalchemy.ext.declarative import declared_attr
from formalchemy import Column

from pyramid.security import authenticated_userid

from osiris.admin.interface import IModel
from osiris.auth import get_current_user

__all__ = ['BaseModel']


def get_current_username():
    from pyramid.threadlocal import get_current_request
    request = get_current_request()
    return authenticated_userid(request) or ""


@implementer(IModel)
class BaseModel(object):
    @declared_attr
    def __tablename__(cls):
        name = re.sub(r'Model$', '', cls.__name__)
        name = "_".join([m.group(1).lower()
                         for m in re.finditer(r'([A-Z][^A-Z]*|[^A-Z]+)', name)])
        return name

    id = Column(
        Integer, primary_key=True,
        label="ID",
        autoincrement=True)

    created_at = Column(
        DateTime,
        label=u"作成日時",
        default=sql.func.now())
    modified_at = Column(
        DateTime,
        label=u"更新日時",
        default=sql.func.now(),
        onupdate=datetime.datetime.now)
    creator_name = Column(
        Text, nullable=False,
        label=u"作成者",
        default=get_current_username)
    modifier_name = Column(
        Text, nullable=False,
        label=u"更新者",
        default=get_current_username,
        onupdate=get_current_username)
