from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from zope.sqlalchemy import ZopeTransactionExtension

__all__ = ['DBSession', 'BaseModel']

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
BaseModel = declarative_base()
