# coding=utf-8
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import ListView, FormView, CreateView, TemplateView, UpdateView
from django.shortcuts import render, redirect
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from utils import change_comma_by_dot
from .models import (
    Segmento, Gasto, Rabbiit, HoraTrabalhada, City,
    Pecas, Itenspecas, Comercio
)
from .forms import (
    SegmentoForm, GastoForm, RabbiitForm,
    PecasForm, ComercioForm, ItensPecasForm, ItemPecasFormSet
)
from vendor.cruds_adminlte.crud import CRUDView
import json
import pandas as pd
from datetime import date, timedelta, datetime
from . import guiabolso


# def GastoComRequest(request):
#     if request.method == 'POST':
#         form = ResultsForm(request.POST)
#         if form.is_valid():
#             form.save()
#         if 'Save_and_add_another' in request.POST:
#             subjectID = form.fields['subjectID']
#             prepop = {'subjectID': subjectID}
#             form = ResultsForm(initial=prepop)
#             return render(request, 'slideAdmin/addResults.html', {'form': form})
#         elif 'Save_and_return' in request.POST:
#             return HttpResponseRedirect('/home/')
#     else:
#         form = ResultsForm()
#     return render(request, 'slideAdmin/addResults.html', {'form': form})

class GastoCRUD(CRUDView):
    model = Gasto
    template_name_base = 'ccruds'
    namespace = None
    check_perms = True
    views_available = ['create', 'list', 'delete', 'update']
    fields = ['name', 'slug', 'valor', 'nro_da_parcela', 'valor_da_parcela', 'parcelas', 'datagasto',]
    list_fields = ('name', 'parcelas', 'nro_da_parcela', 'valor_da_parcela', 'valor', 'datagasto', 'segmento',)
    search_fields = ('name__icontains',)
    paginate_by = 10
    paginate_template = 'cruds/pagination/prev_next.html'

    add_form = GastoForm
    update_form = GastoForm


@receiver(post_save, sender=Gasto)
def _order_post_save(sender, instance, created, **kwargs):
    if created:
        # cont_parcelas = 2
        for cont_parcelas in range(2, instance.parcelas):
        # while instance.parcelas > 1:
            day = 30 * cont_parcelas - 30
            gasto = Gasto()
            gasto.name = instance.name
            gasto.slug = instance.slug
            gasto.valor = instance.valor
            gasto.datagasto = instance.datagasto + timedelta(days=day)
            gasto.segmento = instance.segmento
            gasto.parcelas = cont_parcelas
            gasto.save()
            cont_parcelas += 1
    # if not created:
        # gasto = Gasto.objects.get(id=instance.id)
        # day = 30 * instance.nro_da_parcela
        # datagasto = instance.datagasto + timedelta(days=day)
        # Gasto.objects.filter(id=instance.id).update(datagasto=datagasto)
        # gasto.segmento = instance.segmento
        # gasto.save()


class SegmentoCRUD(CRUDView):
    model = Segmento
    template_name_base = 'ccruds'
    namespace = None
    check_perms = True
    views_available = ['create', 'list', 'delete', 'update']
    list_fields = ['name',]
    search_fields = ['name__icontains']
    split_space_search = ' ' # default False
    add_form = SegmentoForm
    update_form = SegmentoForm


class RabbiitCRUD(CRUDView):
    model = Rabbiit
    template_name_base = 'ccruds'
    namespace = None
    check_perms = True
    views_available = ['create', 'list', 'delete', 'update']
    list_fields = [
        'created_at', 'description', 'time_start',
        'time_end', 'time_total', 'rate_hour',
        'rate_total',
    ]
    search_fields = ['description__icontains']
    add_form = RabbiitForm
    update_form = RabbiitForm


class HoraTrabalhadaCRUD(CRUDView):
    model = HoraTrabalhada
    template_name_base = 'ccruds'
    namespace = None
    check_perms = True
    views_available = ['create', 'list', 'delete', 'update']
    fields = ['id', 'price', ]
    list_fields = ['id', 'price', ]


class CityCRUD(CRUDView):
    model = City
    template_name_base = 'ccruds'
    namespace = None
    check_perms = True
    views_available = ['create', 'list', 'delete', 'update']
    fields = ['id', 'description', ]
    list_fields = ['id', 'description', ]


class PecasListView(TemplateView):
    model = Pecas
    template_name = 'website/pecas_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset_list = Pecas.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(comercio__icontains=query) |
                Q(data__icontains=query)
            ).distinct()

        paginator = Paginator(queryset_list, 5)  # Show 5 pecas per page
        page = self.request.GET.get('page')
        try:
            queryset_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queryset_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 999), deliver last page of results.
            queryset_list = paginator.page(paginator.num_pages)

        return queryset_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_pecas = Pecas.objects.order_by('-id')
        # queryset_list = Pecas.objects.all()
        query = self.request.GET.get("q")
        if query:
            list_pecas = list_pecas.filter(
                Q(comercio__description__icontains=query) |
                Q(data__icontains=query)
            ).distinct()
        paginator = Paginator(list_pecas, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)
        context['object_list'] = object_list
        # context['object_list'] = Pecas.objects.order_by('-id')
        return context


class PecasCreateView(CreateView):
    model = Pecas
    template_name = 'website/pecas_create.html'
    form_class = PecasForm

    def get_context_data(self, **kwargs):
        context = super(PecasCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['forms'] = PecasForm(self.request.POST)
            context['formset'] = ItemPecasFormSet(self.request.POST)
        else:
            context['forms'] = PecasForm()
            context['formset'] = ItemPecasFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        forms = context['forms']
        formset = context['formset']
        if forms.is_valid() and formset.is_valid():
            self.object = form.save()
            forms.instance = self.object
            formset.instance = self.object
            forms.save()
            formset.save()
            return redirect('website_pecas_list')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class PecasEditView(UpdateView):
    model = Pecas
    template_name = 'website/pecas_create.html'
    form_class = PecasForm

    def get_context_data(self, **kwargs):
        context = super(PecasEditView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['forms'] = PecasForm(self.request.POST, instance=self.object)
            context['formset'] = ItemPecasFormSet(self.request.POST, instance=self.object)
        else:
            context['forms'] = PecasForm(instance=self.object)
            context['formset'] = ItemPecasFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form = context['forms']
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            sizeIensPecas = len(formset.cleaned_data)
            total = 0.00
            for chave in range(sizeIensPecas):
                try:
                    total += float(formset.cleaned_data[chave]['subtotal'])
                except:
                    ...
            try:
                form.cleaned_data['total'] = str(total)
            except Exception as err:
                form.cleaned_data['total'] = 0
                print(f'Err.: {err}')
            # form = form.save(commit=False)
            # form.total = str(total)
            form.save()
            formset.save()
            return redirect('website_pecas_list')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ItensPecasCRUD(CRUDView):
    model = Itenspecas
    template_name_base = 'ccruds'
    form_class = PecasForm
    namespace = None
    check_perms = True
    views_available = ['create', 'list', 'delete', 'update']
    fields = ['description', 'pecas','price', 'quantity','subtotal',]
    list_fields = ['id', 'description', 'pecas','price', 'quantity','subtotal',]
    # inlines = [Itenspecas_AjaxCRUD, ]
    add_form = ItensPecasForm
    update_form = ItensPecasForm
    paginate_by = 40

class ComercioCRUD(CRUDView):
    model = Comercio
    template_name_base = 'ccruds'  # customer cruds => ccruds
    namespace = None
    # search_fields = ('head__name__icontains', 'head__email__icontains')
    check_perms = True
    views_available = ['create', 'list', 'update', 'delete', ]
    fields = ['description']
    list_fields = ('id', 'description', )
    add_form = ComercioForm
    update_form = ComercioForm


class GastoSegmentoListView(ListView):

    template_name = "website/gastosPorSegmento.html"
    context_object_name = "gastos"
    paginate_by = 5

    def get_queryset(self):
        slug = 'supermercados'
        resultado = Gasto.objects.filter(segmento__slug=slug)
        # resultado = Gasto.objects.filter(segmento__slug=self.kwargs['slug'])
        return resultado

    def get_context_data(self, **kwargs):
        context = super(GastoSegmentoListView, self).get_context_data(**kwargs)
        list_exam = Gasto.objects.all()
        context['current_segmento'] = list_exam
        return context


# RELATÓRIO DE GASTOS POR MÊS
# ----------------------------------------------

def gastosPorMesView(request):
    template = "website/gastosPorMes.html"
    qs = Gasto.objects.all()  # Use the Pandas Manager
    segmentos = Segmento.objects.all()
    if request.method == 'POST':
        segmento_id = int(request.POST.get('segmento_id'))
        dtInicial = request.POST.get('dtInicial')
        dtFinal = request.POST.get('dtFinal')
        valor = request.POST.get('valor')
        if dtInicial == '':
            dtInicial = '2018-01-01'
        if dtFinal == '':
            dtFinal = date.today()
        df = qs.filter(segmento_id=segmento_id) \
            .to_dataframe(
                ['id', 'name', 'datagasto', 'valor', 'segmento_id'],
                index='segmento_id'
            )
        if valor:
            if not ',' in valor:
                valor = ''.join((valor,',00'))
            df = df.loc[(df['valor'] == str(valor))]
            # df = df.loc[df['valor'] == '50,00']
        df['valor'] = [change_comma_by_dot(e) for e in df['valor']]
        # df['valor'] = [e.replace(",", ".") for e in df['valor']]
        df['valor'] = df['valor'].astype('float')
        df['datagasto'] = pd.to_datetime(df['datagasto'])
        df = df.loc[(df['datagasto'] >= dtInicial) & (df['datagasto'] <= dtFinal)]
        # df['valor'].loc[(df['datagasto'] >= dtInicial) & (df['datagasto'] <= dtFinal)].sum()
        """Format the column headers for the Bootstrap table, 
        they're just a list of field names,
        duplicated and turned into dicts like this: {'field': 'foo', 'title: 'foo'}
        columns = [{'field': f, 'title': f} for f in Gasto._Meta.fields]
        columns = [{'field': f['_verbose_name'], 'title': f} for f in Gasto._meta.fields]
        """
        col = [f for f in Gasto._meta.get_fields()]
        columns = [{'field': f, 'title': f} for f in df.columns]
        """Write the DataFrame to JSON (as easy as can be)
            output just the records (no fieldnames) as a collection of tuples
            Proceed to create your context object containing the columns and the data"""

        # data = df.to_json(orient='records', lines=True)
        context = {
            'data': df.itertuples(),
            'segmentos': segmentos
        }
    else:
        context = {
            'segmentos': segmentos
        }
    return render(request, template, context)
    # title = 'Lista de Gastos por Mês'
    # html_string = '''
    # {% extends "_base.html" %}
    #   <body>
    #     {table}
    #   </body>
    # '''
    # return HttpResponse(df.to_html())
    # return HttpResponse(
    #     html_string.format(
    #         table=df.to_html(classes='table table-striped')
    #     )
    # )



# GUIABOLSO scripts
# ----------------------------------------------

def guiaBolsoView(request):
    template = "website/guiabolso.html"
    context = {}
    # from django.conf import settings
    # env = settings.env
    import os
    if request.method == 'POST':
        gb = guiabolso.GuiaBolsoSelenium()
        url = 'https://www.guiabolso.com.br/web/#/login'
        params = {}
        params['email'] = os.environ['GUIABOLSO_EMAIL']
        params['password'] = os.environ['GUIABOLSO_PASSWORD']
        get_data = gb.main(url, params)
        print(get_data)
        context = {
            'lista_dos_gastos': get_data
        }
        print('Tudo OK!')
    return render(request, template, context)

# CADASTRAMENTO DE GASTOS
# ----------------------------------------------


class AutoCompleteView(FormView):
    def get(self, request):
        q = request.GET.get('term', '').capitalize()
        if q:
            gastos = Gasto.objects.filter(name__icontains=q).order_by('name').distinct('name')
            # gastos = Gasto.objects.filter(name__icontains=q).distinct('name')
        else:
            gastos = Gasto.objects.all()
        results = []
        for gasto in gastos:
            if results:
                if gasto.name not in results[0]['name']:
                    gasto_json = {}
                    gasto_json['name'] = gasto.name
                    results.append(gasto_json)
            else:
                gasto_json = {}
                gasto_json['name'] = gasto.name
                results.append(gasto_json)
        data = json.dumps(results)
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)


class AutoResponseView(ListView):
    ...
