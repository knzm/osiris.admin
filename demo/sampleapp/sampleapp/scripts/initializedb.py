# -*- coding: utf-8 -*-

import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from sampleapp.models import (
    DBSession,
    BaseModel,
    UserModel,
    GroupModel,
    NewsModel,
    )

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def setup_news():
    entity = NewsModel(title=u"Hello, world!", body=u"This is a news.")
    DBSession.add(entity)

def setup_user():
    users = [
        ("admin@example.com", "test", "admin"),
        ("user@example.com", "test", "user"),
        ("guest@example.com", "test", "guest"),
        ]

    groups = {}
    for username, password, group_name in users:
        user = UserModel(username=username)
        user.password = password
        DBSession.add(user)
        if group_name not in groups:
            group = GroupModel(group_name=group_name)
            DBSession.add(group)
            groups[group_name] = group
        user.groups.append(groups[group_name])

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)

    config_uri = argv[1]
    setup_logging(config_uri)

    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    BaseModel.metadata.create_all(engine)
    with transaction.manager:
        if DBSession.query(NewsModel).count() == 0:
            setup_news()

        if DBSession.query(UserModel).count() == 0 and \
                DBSession.query(GroupModel).count() == 0:
            setup_user()
