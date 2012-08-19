# -*- coding: utf-8 -*-

from zope.interface import provider

from sqlalchemy import Table, Column, Integer, Unicode, String, ForeignKey
from sqlalchemy.orm import relationship

from osiris.auth.interface import IUserModel, IGroupModel
from osiris.auth.models import UserMixin

from .base import BaseModel

__all__ = ['UserModel', 'GroupModel', 'user_group']

user_group = Table(
    "user_group", BaseModel.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('group_id', Integer, ForeignKey('group.id')),
    )


@provider(IUserModel)
class UserModel(BaseModel, UserMixin):
    username = Column(Unicode(255), unique=True)
    _password = Column("password", String(255))


@provider(IGroupModel)
class GroupModel(BaseModel):
    group_name = Column(Unicode(255), unique=True)
    users = relationship('UserModel', backref="groups",
                         secondary=user_group)


def includeme(config):
    config.registry.registerUtility(UserModel, IUserModel)
    config.registry.registerUtility(GroupModel, IGroupModel)
