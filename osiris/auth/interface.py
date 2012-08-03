# -*- coding: utf-8 -*-

from zope.interface import Interface, Attribute


class IAccountView(Interface):
    def login_form(self):
        """ show login form """

    def login(self):
        """ process login request """

    def logout(self):
        """ process logout request """


class IUserModel(Interface):
    username = Attribute("User name")
    password = Attribute("Password (write-only)")
    groups = Attribute("List of groups")

    def verify_password(self, password):
        """Return True if password is valid for this user"""


class IGroupModel(Interface):
    group_name = Attribute("Group name")
    users = Attribute("List of users")

