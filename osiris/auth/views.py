# -*- coding: utf-8 -*-

from zope.interface import implementer
from pyramid.security import remember, forget, authenticated_userid
from pyramid.httpexceptions import HTTPFound

from .security import authenticate
from .interface import IAccountView


@implementer(IAccountView)
class AccountView(object):
    admin_route_name = 'admin_redirect'

    def __init__(self, request):
        self.request = request

    def login_form(self):
        if authenticated_userid(self.request):
            location = self.request.route_url(self.admin_route_name)
            return HTTPFound(location=location)

        form_value = self.get_form_value()
        return self.render(
            location=form_value['location'],
            username=form_value['username'],
            # For security reason, we refuse to use the password
            # passed via GET parameter.
            password="")

    def login(self):
        if authenticated_userid(self.request):
            location = self.request.route_url(self.admin_route_name)
            return HTTPFound(location=location)

        form_value = self.get_form_value()
        location = form_value['location']
        username = form_value['username']
        password = form_value['password']

        user = authenticate(username, password, self.request)

        if user:
            headers = remember(self.request, username)
            return HTTPFound(location=location, headers=headers)

        return self.render(
            location=location,
            username=username,
            password=password,
            message="Login Failed")

    def logout(self):
        headers = forget(self.request)
        location = self.request.route_url('login')
        return HTTPFound(location=location, headers=headers)

    def render(self, **context):
        login_url = self.request.route_url('login')
        context['login_url'] = login_url
        context['title'] = "Login"
        if 'message' not in context:
            context['message'] = ""
        return context

    def get_form_value(self):
        login_url = self.request.route_url('login')
        referrer = self.request.url
        if referrer == login_url:
            # never use the login form itself as came_from
            referrer = self.request.route_url('login')
        location = self.request.params.get('location', referrer)

        username = self.request.params.get('username', "")
        password = self.request.params.get('password', "")

        return {
            'location': location,
            'username': username,
            'password': password,
            }
