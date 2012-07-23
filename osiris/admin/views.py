# -*- coding: utf-8 -*-

from zope.interface import implementer, provider
from webhelpers.paginate import Page
from formalchemy.fields import _pk
from pyramid import httpexceptions as exc
from pyramid.exceptions import NotFound
from pyramid.i18n import get_locale_name
# from pyramid_formalchemy import actions
from fa.bootstrap import actions
# from pyramid_formalchemy.utils import TemplateEngine

from osiris.admin.interface import (
    IModelIndexView,
    IModelListView,
    IModelItemView,
    IModelIndexViewFactory,
    IModelListViewFactory,
    IModelItemViewFactory,
    IModelGrid,
    IModelForm,
    IModelAddForm,
    IModelEditForm,
    IModelViewForm,
    )


class BaseModelView(object):

    # engine = TemplateEngine()

    actions_categories = ('buttons',)
    defaults_actions = actions.defaults_actions

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.session = request.session_factory

        if '_LOCALE_' not in request.cookies:
            locale = get_locale_name(request)
            request.cookies['_LOCALE_'] = locale
        if '_LOCALE_' not in request.cookies:
            theme = request.registry.settings.get(
                'default_theme_name', 'smoothness')
            request.cookies['_LOCALE_'] = theme

    # def breadcrumb(self, form=None, **kwargs):
    #     request = self.request
    #     model_name = request.model_name
    #     items = []
    #     items.append((request.fa_url(), 'root', 'root_url'))
    #     if request.model_name:
    #         items.append((request.fa_url(model_name), model_name, 'model_url'))
    #     return items

    def update_resources(self):
        """A hook to add some fanstatic resources"""
        from js import jqueryui
        from js import jqgrid
        from fa.jquery.fanstatic_resources import fa_jqgrid

        cookie = getattr(self.request, 'cookies', {})

        # default_theme = 'smoothness'
        # theme = cookie.get('_THEME_', default_theme)
        # try:
        #     jqueryui_theme = getattr(jqueryui, theme)
        # except AttributeError:
        #     pass
        # else:
        #     jqueryui_theme.need()

        # fa_admin.need()

        lang = cookie.get('_LOCALE_', 'en')
        jqgrid_i18n = getattr(jqgrid, 'jqgrid_i18n_%s' % lang,
                              jqgrid.jqgrid_i18n_en)
        jqgrid_i18n.need()

        fa_jqgrid.need()

    def render(self, **kwargs):
        request = self.request
        if request.format != 'html':
            meth = getattr(self, 'render_%s_format' % request.format, None)
            if meth is not None:
                return meth(**kwargs)
            else:
                raise NotFound()

        # if request.model_class:
        #     from pyramid_formalchemy.i18n import I18NModel
        #     request.model_class = model_class = I18NModel(
        #         request.model_class, request)
        #     request.model_label = model_label = model_class.label
        #     request.model_plural = model_plural = model_class.plural
        # else:
        #     model_class = request.model_class
        #     model_label = model_plural = ''

        # from pyramid_formalchemy.i18n import I18NModel
        # model_label = I18NModel(request.model_class, request).label
        # request.model_label = model_label

        self.update_resources()

        kwargs.update(
            model_class=request.model_class,
            model_name=request.model_name,
            # model_label=model_label,
            # model_plural=model_plural,
            actions=request.actions,
            title=request.context.title,
            )

        return kwargs


@provider(IModelIndexViewFactory)
@implementer(IModelIndexView)
class ModelIndexView(BaseModelView):

    def index(self, **kwargs):
        request = self.request
        return self.render()


@provider(IModelListViewFactory)
@implementer(IModelListView)
class ModelListView(BaseModelView):

    pager_args = dict(
        link_attr={
            'class': 'ui-pager-link ui-state-default ui-corner-all',
            },
        curpage_attr={
            'class': 'ui-pager-curpage ui-state-highlight ui-corner-all',
            })

    @actions.action('listing')
    def index(self, **kwargs):
        """listing page"""
        page = self.get_page(**kwargs)

        grid = self.get_grid()
        grid.bind(instances=page, session=self.session, request=self.request)

        if 'pager' not in kwargs:
            pager = page.pager(**self.pager_args)
        else:
            pager = kwargs.pop('pager')

        return self.render_grid(grid=grid, pager=pager)

    def get_page(self, **kwargs):
        request = self.request
        def get_page_url(page, partial=None):
            url = "%s?page=%s" % (self.request.path, page)
            if partial:
                url += "&partial=1"
            return url
        options = dict(page=int(request.GET.get('page', '1')),
                       url=get_page_url)
        options.update(kwargs)
        if 'collection' not in options:
            query = self.session.query(request.model_class)
            options['collection'] = request.query_factory(request, query)
        collection = options.pop('collection')
        return Page(collection, **options)

    def get_grid(self):
        """return a Grid object"""
        request = self.request
        grid = request.registry.getAdapter(request.model_class, IModelGrid)
        # if not grid.engine:
        #     grid.engine = self.engine
        return grid

    def render_grid(self, **kwargs):
        """render the grid as html or json"""
        return self.render(is_grid=True, **kwargs)


@provider(IModelItemViewFactory)
@implementer(IModelItemView)
class ModelItemView(BaseModelView):

    @actions.action()
    def show(self):
        request = self.request

        instance = request.model_instance
        if not instance:
            raise NotFound()

        form = self.get_form(IModelViewForm)
        form.bind(model=instance)

        return self.render(form=form)

    @actions.action()
    def new(self):
        request = self.request
        form = self.get_form(IModelAddForm)
        return self.render(form=form)

    @actions.action('new')
    def create(self):
        request = self.request

        form = self.get_form(IModelAddForm)
        form.bind(data=request.POST)

        if not form.validate():
            return self.render(form=form)

        form.sync()
        self.session.add(form.model)
        self.session.flush()

        location = request.fa_url(request.model_name)
        return exc.HTTPFound(location=location)

    @actions.action()
    def edit(self):
        request = self.request

        instance = request.model_instance
        if not instance:
            raise NotFound()

        form = self.get_form(IModelEditForm)
        form.bind(model=instance)

        return self.render(form=form)

    @actions.action('edit')
    def update(self):
        request = self.request

        instance = request.model_instance
        if not instance:
            raise NotFound()

        form = self.get_form(IModelEditForm)
        form.bind(model=instance, data=request.POST)

        if not form.validate():
            return self.render(form=form)

        form.sync()
        self.session.merge(form.model)
        self.session.flush()

        location = request.fa_url(request.model_name, _pk(instance))
        return exc.HTTPFound(location=location)

    def delete(self):
        request = self.request

        instance = request.model_instance
        if not instance:
            raise NotFound()

        self.session.delete(instance)

        location = request.fa_url(request.model_name)
        return exc.HTTPFound(location=location)

    def get_form(self, form_interface):
        request = self.request
        form = request.registry.getAdapter(request.model_class, form_interface)
        # if not form.engine:
        #     form.engine = self.engine
        form.bind(session=self.session, request=request)
        return form


def includeme(config):
    config.registry.registerUtility(ModelIndexView, IModelIndexViewFactory)
    config.registry.registerUtility(ModelListView, IModelListViewFactory)
    config.registry.registerUtility(ModelItemView, IModelItemViewFactory)
