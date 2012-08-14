# -*- coding: utf-8 -*-

import functools

import tw2.core as twc
from tw2.forms import LinkField
from tw2.jquery import jquery_js

from pyramid.decorator import reify
from pyramid.security import has_permission

def _(s): return s

__all__ = [
    'RequestActions', 'UIButton', 'defaults_actions', 'action',
]


class RequestActions(dict):

    def __getattr__(self, attr):
        actions = self.get(attr, [])
        if actions:
            def render(request, **kw):
                return self.render(request, actions, **kw)
            return render
        return None

    def render(self, request, actions, **kw):
        allowed_actions = []
        for a in actions:
            if a.permission is None or \
                    has_permission(a.permission, request.context, request):
                allowed_actions.append(a)
        return "\n".join([w.display(**kw) for w in allowed_actions])


class UIButton(LinkField):
    permission = None
    onclick = None
    value = True

    @reify
    def request(self):
        from pyramid.threadlocal import get_current_request
        return get_current_request()

    def prepare(self):
        super(UIButton, self).prepare()
        if self.onclick:
            self.safe_modify('attrs')
            self.attrs['onclick'] = self.onclick


class NewButton(UIButton):
    permission = 'new'
    text = _('New')
    css_class = 'btn btn-primary'

    def prepare(self):
        self.safe_modify('link')
        link = self.request.fa_url(self.request.model_name, 'new')
        self.link = link
        # self.safe_modify('text')
        # self.text = _('New %s') % self.request.model_label
        super(NewButton, self).prepare()


class SaveButton(UIButton):
    permission = 'edit'
    text = _('Save')
    css_class = 'btn btn-success'
    link = "#"
    onclick = "jQuery(this).parents('form').submit();"
    resources = [jquery_js]


class SaveAndAddAnotherButton(UIButton):
    permission = 'edit'
    text = _('Save and add another')
    css_class = 'btn btn-success'
    onclick = ("var f = jQuery(this).parents('form');"
               "jQuery('#next', f).val(window.location.href);"
               "f.submit();")
    resources = [jquery_js]


class EditButton(UIButton):
    permission = 'edit'
    text = _('Edit')
    css_class = 'btn btn-info'

    def prepare(self):
        self.safe_modify('link')
        link = self.request.fa_url(self.request.model_name,
                                   self.request.model_id, 'edit')
        self.link = link
        super(EditButton, self).prepare()


class BackButton(UIButton):
    text = _('Back')
    css_class = 'btn'

    def prepare(self):
        self.safe_modify('link')
        link = self.request.fa_url(self.request.model_name)
        self.link = link
        super(BackButton, self).prepare()


class DeleteButton(UIButton):
    permission = 'delete'
    text = _('Delete')
    css_class = 'btn btn-danger'
    onclick = ("var f = jQuery(this).parents('form');"
               "f.attr('action', window.location.href.replace('/edit', '/delete'));"
               "f.submit();")
    resources = [jquery_js]


class CancelButton(UIButton):
    permission = 'view'
    text = _('Cancel')
    css_class = 'btn'

    def prepare(self):
        self.safe_modify('link')
        link = self.request.fa_url(self.request.model_name)
        self.link = link
        super(CancelButton, self).prepare()


new = NewButton('new')
save = SaveButton('save')
save_and_add_another = SaveAndAddAnotherButton('save_and_add_another')
edit = EditButton('edit')
delete = DeleteButton('delete')
back = BackButton('back')
cancel = CancelButton('cancel')

defaults_actions = {
    "listing": [new],
    "new": [save, save_and_add_another, cancel],
    "show": [edit, back],
    "edit": [save, delete, cancel],
    }


class action(object):
    """A decorator use to add some actions to the request.
    """
    def __init__(self, name=None):
        self.name = name

    def __call__(self, func):
        action = self.name or func.__name__

        @functools.wraps(func)
        def wrapped(self, *args, **kwargs):
            request = self.request
            if request.format in ('html', 'xhr') and \
                    request.model_class is not None:
                request.action = func.__name__
                actions = defaults_actions.get(action, [])
                request.actions['buttons'] = actions
            return func(self, *args, **kwargs)

        return wrapped
