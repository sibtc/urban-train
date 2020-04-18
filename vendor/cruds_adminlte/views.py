# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured

from django.apps import apps
from django.urls import (
    NoReverseMatch,
    reverse,
)
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from django.db.models.constants import LOOKUP_SEP
from django.db import models
from django.db.models import Q

from django.utils.decorators import method_decorator

from django.utils.translation import ugettext as _

from django.shortcuts import redirect

from django.contrib.admin.views.main import IGNORED_PARAMS
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from . import utils


class CRUDMixin(object):
    crud_template_name = None
    can_delete = None
    required_permissions = ()

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        #this will be passed in get_context
        self.can_delete = request.user.has_perm(self.get_delete_perm_string())
        #return message error case permission not present
        if not request.user.has_perms(self.required_permissions):
            messages.error(
                request,
                _('Você não tem permissão para acessar a funcionalidade.'),
                extra_tags='alert-danger'
                  )
            return redirect('/')
        return super(CRUDMixin, self).dispatch(
            request, *args, **kwargs)

    def get_delete_perm_string(self):
        #return 'app.delete_model' string
        return '{}.delete_{}'.format(self.model._meta.app_label.lower(), self.model.__name__.lower())

    def get_context_data(self, **kwargs):
        """
        Adds available urls and names.
        """
        context = super(CRUDMixin, self).get_context_data(**kwargs)
        context.update({
            'model_verbose_name': self.model._meta.verbose_name,
            'model_verbose_name_plural': self.model._meta.verbose_name_plural,
            'search_fields': getattr(self, 'search_fields', None),
            'can_delete': self.can_delete,
        })

        try:
            context['fields'] = utils.get_fields(self.model, include=self.list_display)
        except AttributeError:
            context['fields'] = utils.get_fields(self.model)

        if hasattr(self, 'object') and self.object:
            for action in utils.INSTANCE_ACTIONS:
                try:
                    url = reverse(
                        utils.crud_url_name(self.model, action),
                        kwargs={'pk': self.object.pk})
                except NoReverseMatch:
                    url = None
                context['url_%s' % action] = url

        for action in utils.LIST_ACTIONS:
            try:
                url = reverse(
                    utils.crud_url_name(self.model, action)
                )
            except NoReverseMatch:
                url = None
            context['url_%s' % action] = url

        return context

    def get_template_names(self):
        """
        Adds crud_template_name to default template names.
        """
        names = super(CRUDMixin, self).get_template_names()
        if self.crud_template_name:
            names.append(self.crud_template_name)
        return names


class CRUDCreateView(CreateView):
    template_name = 'add_form.html'
    success_message = "%(nome)s foi criado com sucesso."

    def __init__(self, *args, **kwargs):
        super(CRUDCreateView, self).__init__(*args, **kwargs)
        #add app.add_model permission
        self.required_permissions = (
             '{}.add_{}'.format(self.form_class._meta.model._meta.app_label.lower(),
                                self.form_class._meta.model.__name__.lower()),
         )
    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        context = super(CRUDCreateView, self).get_context_data(**kwargs)

        context.update({
            'model_verbose_name': self.form_class._meta.model._meta.verbose_name,
            'model_verbose_name_plural': self.form_class._meta.model._meta.verbose_name_plural,
        })

        #try:
        context['fields'] = utils.get_fields(self.form_class._meta.model)
        # except AttributeError:
        #     context['fields'] = utils.get_fields(self.form_class._meta.model)

        if hasattr(self, 'object') and self.object:
            for action in utils.INSTANCE_ACTIONS:
                try:
                    url = reverse(
                        utils.crud_url_name(self.form_class._meta.model, action),
                        kwargs={'pk': self.form_class._meta.object.pk})
                except NoReverseMatch:
                    url = None
                context['url_%s' % action] = url

        for action in utils.LIST_ACTIONS:
            try:
                url = reverse(
                    utils.crud_url_name(self.form_class._meta.model, action)
                )
            except NoReverseMatch:
                url = None
            context['url_%s' % action] = url

        return context


    def form_valid(self, form):
        response = super(CRUDCreateView, self).form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

    required_permissions = ()

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perms(self.required_permissions):
            messages.error(
                request,
                _('Você não tem permissão para acessar a funcionalidade.'),
                extra_tags='alert-danger'
            )
            return redirect('/')
        return super(CRUDCreateView, self).dispatch(
            request, *args, **kwargs)


class CRUDDeleteView(CRUDMixin, DeleteView):
    crud_template_name = 'delete.html'

    def __init__(self, *args, **kwargs):
        super(CRUDDeleteView, self).__init__(*args, **kwargs)
        #add app.delete_model permission
        self.required_permissions = (
             '{}.delete_{}'.format(self.model._meta.app_label.lower(),
                                self.model.__name__.lower()),
         )


class CRUDDetailView(CRUDMixin, DetailView):
    crud_template_name = 'cruds/detail.html'

    def get_filters_params(self, params=None):
        """
        Returns all params except IGNORED_PARAMS
        """
        if not params:
            params = self.params
        lookup_params = params.copy()  # a dictionary of the query string {'rede__id__exact':'1'}
        # Remove all the parameters that are globally and systematically
        # ignored.
        for ignored in IGNORED_PARAMS:
            if ignored in lookup_params:
                del lookup_params[ignored]
        return lookup_params

    def get_queryset(self):
        qs = super(CRUDDetailView, self).get_queryset()
        self.params = dict(self.request.GET.items())

        self.lookup_params = self.get_filters_params()

        filters = {}

        self.fields = [f.name for f in self.model._meta.fields]
        for p in self.lookup_params:
            if LOOKUP_SEP in p:
                field_name = p.split(LOOKUP_SEP)[0]
                if field_name in self.fields:
                    if isinstance(self.model._meta.get_field(field_name), models.ForeignKey):
                        field_name, related_field, field_qterm = p.split(LOOKUP_SEP)
                    else:
                        field_name, field_qterm = p.split(LOOKUP_SEP)
            else:
                field_name = ''

            if field_name in self.fields:
                if self.request.GET.get(p) != '':
                    filters[p] = self.request.GET.get(p)
        try:
            qs = qs.filter(**filters)
        except ValueError:
            raise ImproperlyConfigured

        if self.request.GET.get('q', '') and self.search_fields:
            self.query = '|'.join(
                ['Q({}__icontains="{}")'.format(
                    f, self.request.GET.get('q', '')) for f in self.search_fields]
            )
            qs = qs.filter(eval(self.query))

        return qs

class CRUDListView(CRUDMixin, ListView):
    params = None
    list_filter = None
    crud_template_name = 'change_list.html'
    search_fields = None
    query = None
    lookup_params=None

    def __init__(self, *args, **kwargs):
        super(CRUDListView, self).__init__(*args, **kwargs)
        #add app.change_model permission
        self.required_permissions = (
             '{}.change_{}'.format(self.model._meta.app_label.lower(), self.model.__name__.lower()),
         )

    def get_success_url(self):
        return reverse(
            utils.crud_url_name(self.model, utils.ACTION_LIST))

    def get_filters_params(self, params=None):
        """
        Returns all params except IGNORED_PARAMS
        """
        if not params:
            params = self.params
        lookup_params = params.copy()  # a dictionary of the query string {'rede__id__exact':'1'}
        # Remove all the parameters that are globally and systematically
        # ignored.
        for ignored in IGNORED_PARAMS:
            if ignored in lookup_params:
                del lookup_params[ignored]
        return lookup_params

    def get_context_data(self, **kwargs):
        context = super(CRUDListView, self).get_context_data(**kwargs)
        fields_list_filter=[]
        if self.list_filter:
            for field_name in self.list_filter:
                if field_name in self.fields:
                    field = self.model._meta.get_field(field_name)
                    internal_type = field.get_internal_type()
                    if internal_type=='BooleanField':
                        fields_list_filter.append((field, internal_type, field.choices  ))
                    if internal_type=='ForeignKey':
                        fields_list_filter.append((field, internal_type, field.related_model.objects.all()))

        context.update({
            'fields_list_filter': fields_list_filter,
            'querystring': self.request.GET.urlencode(),
            'q': self.request.GET.get('q', ''),
            'context_menu': self.context_menu,
        })

        return context

    def get_queryset(self):
        qs = super(CRUDListView, self).get_queryset()
        self.params = dict(self.request.GET.items())

        self.lookup_params = self.get_filters_params()

        filters = {}

        self.fields = [f.name for f in self.model._meta.fields]
        for p in self.lookup_params:
            if LOOKUP_SEP in p:
                field_name = p.split(LOOKUP_SEP)[0]
                if field_name in self.fields:
                    if isinstance(self.model._meta.get_field(field_name), models.ForeignKey):
                        field_name, related_field, field_qterm = p.split(LOOKUP_SEP)
                    else:
                        field_name, field_qterm = p.split(LOOKUP_SEP)
            else:
                field_name = ''

            if field_name in self.fields:
                if self.request.GET.get(p) != '':
                    filters[p] = self.request.GET.get(p)
        try:
            qs = qs.filter(**filters)
        except ValueError:
            raise ImproperlyConfigured

        if self.request.GET.get('q', '') and self.search_fields:
            self.query = '|'.join(
                ['Q({}__icontains="{}")'.format(
                    f, self.request.GET.get('q', '')) for f in self.search_fields]
            )
            qs = qs.filter(eval(self.query))

        return qs


class CRUDUpdateView(CRUDMixin, UpdateView):
    crud_template_name = 'change_form.html'
    success_message = "%(nome)s foi alterado com sucesso."
    can_delete = None

    def __init__(self, *args, **kwargs):
        super(CRUDUpdateView, self).__init__(*args, **kwargs)
        #add app.change_model permission
        self.required_permissions = (
             '{}.change_{}'.format(self.model._meta.app_label.lower(), self.model.__name__.lower()),
         )

    def form_valid(self, form):
        response = super(CRUDUpdateView, self).form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data
