# -*- coding: utf-8 -*-

import hashlib

from osiris.admin.utils import get_current_dbsession


class UserMixin:

    username = None
    _password = None

    def set_password(self, password):
        self._password = self.hash_password(password)

    password = property(fset=set_password)

    @classmethod
    def get_by_username(cls, username):
        query = get_current_dbsession().query(cls)
        return query.filter_by(username=username).first()

    def verify_password(self, password):
        return self._password == self.hash_password(password)

    @property
    def salt(self):
        # ToDo: add salt
        return ""

    def hash_password(self, password):
        return hashlib.sha1(self.salt + password).hexdigest()
