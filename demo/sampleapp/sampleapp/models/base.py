# -*- coding: utf-8 -*-

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from zope.sqlalchemy import ZopeTransactionExtension

import osiris.admin

__all__ = ['DBSession', 'BaseModel']

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

class BaseModel(declarative_base(cls=osiris.admin.BaseModel)):
    __abstract__ = True
    __table_args__ = {'mysql_engine': 'InnoDB'}
