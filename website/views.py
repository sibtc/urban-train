# coding=utf-8
import json
import re
from datetime import datetime

from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)

from accounts.constants import MESES
from tools.utils import add_one_month, change_comma_by_dot

from . import forms, models


class GastoListView(ListView):
    template_name = "website/gasto/gasto_list.html"
    model = models.Gasto

    def get_context_data(self, **kwargs):
        context = super(GastoListView, self).get_context_data(**kwargs)
        # get_columns_in_the_model = [field.name for field in models.Gasto._meta.get_fields()]
        context["columns"] = [
            "parcelas_gasto",
            "id",
            "name",
            "more_infos",
            "opcoes_cartao",
            "datagasto",
            "total",
            "segmento",
        ]
        context["count"] = self.get_queryset().count()
        return context

    def get_queryset(self):
        queryset = super(GastoListView, self).get_queryset()
        if search := self.request.GET.get("search"):
            RE_INT = re.compile(r"^[-+]?([1-9]\d*|0)$")
            # Essa linha qdo quero trazer o ID
            if RE_INT.match(search):
                queryset = queryset.filter(id=search)
            else:
                queryset = queryset.filter(Q(name__icontains=search))
        return queryset
        # return super().get_queryset().get(id=self.kwargs['pk'])


class GastoCreateView(CreateView):
    model = models.Gasto
    template_name = "website/gasto/gasto_form.html"
    form_class = forms.GastoForm

    def get_context_data(self, **kwargs):
        context = super(GastoCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["forms"] = forms.GastoForm(self.request.POST)
            context["formset"] = forms.ParcelasFormSet(self.request.POST)
        else:
            context["forms"] = forms.GastoForm()
            context["formset"] = forms.ParcelasFormSet()
            context["last_data"] = models.Gasto.objects.first()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        forms = context["forms"]
        formset = context["formset"]
        validated = forms.is_valid()
        if not formset.is_valid() or not validated:
            return self.render_to_response(self.get_context_data(form=form))
        gasto = forms.save(commit=False)
        total = 0.00
        for price in formset.cleaned_data:
            if len(price) > 0:
                vlr_parcela = price["valor_parcela"]
                if "." in vlr_parcela:
                    vlr_parcela = vlr_parcela.replace(".", "")
                total += float(vlr_parcela.replace(",", "."))
        gasto.total = round(total, 2)
        gasto.save()
        formset.instance = gasto
        formset.save()
        return redirect("website_gasto_list")


class GastoEditView(UpdateView):
    model = models.Gasto
    template_name = "website/gasto/gasto_form.html"
    form_class = forms.GastoForm

    def get_context_data(self, **kwargs):
        context = super(GastoEditView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["forms"] = forms.GastoForm(self.request.POST, instance=self.object)
            context["formset"] = forms.ParcelasFormSet(self.request.POST, instance=self.object)
        else:
            context["forms"] = forms.GastoForm(instance=self.object)
            context["formset"] = forms.ParcelasFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        forms = context["forms"]
        formset = context["formset"]
        validated = forms.is_valid()
        if not formset.is_valid() or not validated:
            return self.render_to_response(self.get_context_data(form=form))
        gasto = forms.save(commit=False)
        total = 0.00
        for price in formset.cleaned_data:
            if len(price) > 0:
                total += float(price["valor_parcela"].replace(",", "."))
        gasto.total = round(total, 2)
        gasto.save()
        formset.instance = gasto
        formset.save()
        return redirect("website_gasto_list")


class GastoDeleteView(DeleteView):
    success_url = reverse_lazy("website_gasto_list")
    model = models.Gasto
    template_name_suffix = "/gastos_confirm_delete"


class ComercioListView(ListView):
    template_name = "website/pecas/comercio_list.html"
    model = models.Comercio
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ComercioListView, self).get_context_data(**kwargs)
        # get_columns_in_the_model = [field.name for field in models.Gasto._meta.get_fields()]
        context["columns"] = [
            "parcelas_gasto",
            "id",
            "name",
            "more_infos",
            "opcoes_cartao",
            "datagasto",
            "total",
            "segmento",
        ]
        context["count"] = self.get_queryset().count()
        return context

    def get_queryset(self):
        queryset = super(ComercioListView, self).get_queryset()

        data = self.request.GET

        if search := data.get("search"):
            RE_INT = re.compile(r"^[-+]?([1-9]\d*|0)$")
            # Essa linha qdo quero trazer o ID do gasto
            if RE_INT.match(search):
                queryset = queryset.filter(id=search)
            else:
                queryset = queryset.filter(Q(description__icontains=search))

        return queryset


class ComercioCreateView(CreateView):
    model = models.Comercio
    template_name = "website/pecas/comercio_form.html"
    form_class = forms.ComercioForm

    def get_context_data(self, **kwargs):
        context = super(ComercioCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["forms"] = forms.ComercioForm(self.request.POST)
        else:
            context["forms"] = forms.ComercioForm()
            context["last_data"] = models.Gasto.objects.first()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        forms = context["forms"]
        if not forms.is_valid():
            return self.render_to_response(self.get_context_data(form=form))
        forms.save()
        return redirect("website_comercio_list")


class ComercioEditView(UpdateView):
    model = models.Comercio
    template_name = "website/pecas/comercio_form.html"
    form_class = forms.ComercioForm

    def get_context_data(self, **kwargs):
        context = super(ComercioEditView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["forms"] = forms.ComercioForm(self.request.POST, instance=self.object)
        else:
            context["forms"] = forms.ComercioForm(instance=self.object)
            context["last_data"] = models.Gasto.objects.first()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        forms = context["forms"]
        if not forms.is_valid():
            return self.render_to_response(self.get_context_data(form=form))
        forms.save()
        return redirect("website_comercio_list")


class ComercioDeleteView(DeleteView):
    success_url = reverse_lazy("website_comercio_list")
    model = models.Comercio
    template_name = "website/pecas/comercio_confirm_delete.html"


class CityListView(ListView):
    template_name = "website/pecas/city_list.html"
    model = models.City

    def get_queryset(self):
        return models.City.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CityListView, self).get_context_data(**kwargs)
        list_exam = models.City.objects.all()
        context["current_segmento"] = list_exam
        context["count"] = models.City.objects.count()
        return context


class CityCreateView(CreateView):
    model = models.City
    template_name = "website/pecas/city_form.html"
    form_class = forms.CityForm

    def get_context_data(self, **kwargs):
        context = super(CityCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["forms"] = forms.CityForm(self.request.POST)
        else:
            context["forms"] = forms.CityForm()
            context["last_data"] = models.City.objects.first()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        forms = context["forms"]
        if not forms.is_valid():
            return self.render_to_response(self.get_context_data(form=form))
        forms.save()
        return redirect("website_city_list")


class PecasListView(ListView):
    model = models.Pecas
    template_name = "website/pecas/pecas_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PecasListView, self).get_context_data(**kwargs)
        # get_columns_in_the_model = [field.name for field in models.Gasto._meta.get_fields()]
        context["columns"] = [
            "parcelas_gasto",
            "id",
            "name",
            "more_infos",
            "opcoes_cartao",
            "datagasto",
            "total",
            "segmento",
        ]
        context["count"] = self.get_queryset().count()
        return context

    def get_queryset(self):
        queryset = super(PecasListView, self).get_queryset()
        RE_INT = re.compile(r"^[-+]?([1-9]\d*|0)$")

        data = self.request.GET

        if search := data.get("search"):
            # Essa linha qdo quero trazer o ID do gasto
            if RE_INT.match(search):
                queryset = queryset.filter(id=search)
            else:
                queryset = queryset.filter(Q(comercio__description__icontains=search))

        if type_vehicle := data.get("type_vehicle"):
            queryset = queryset.filter(Q(veiculo=type_vehicle))

        return queryset


class PecasCreateView(CreateView):
    model = models.Pecas
    template_name = "website/pecas/pecas_form.html"
    form_class = forms.PecasForm

    def get_context_data(self, **kwargs):
        context = super(PecasCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["forms"] = forms.PecasForm(self.request.POST)
            context["formset"] = forms.ItemPecasFormSet(self.request.POST)
        else:
            context["forms"] = forms.PecasForm()
            context["formset"] = forms.ItemPecasFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        forms = context["forms"]
        formset = context["formset"]
        if not forms.is_valid() or not formset.is_valid():
            return self.render_to_response(self.get_context_data(form=form))
        pecas = forms.save(commit=False)
        total = 0.00
        for price in formset.cleaned_data:
            total += float(price["subtotal"].replace(",", "."))
        pecas.total = round(total, 2)
        pecas.save()
        formset.instance = pecas
        formset.save()
        return redirect("website_pecas_list")


class PecasEditView(UpdateView):
    model = models.Pecas
    template_name = "website/pecas/pecas_form.html"
    form_class = forms.PecasForm

    def get_context_data(self, **kwargs):
        context = super(PecasEditView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["forms"] = forms.PecasForm(self.request.POST, instance=self.object)
            context["formset"] = forms.ItemPecasFormSet(self.request.POST, instance=self.object)
        else:
            context["forms"] = forms.PecasForm(instance=self.object)
            context["formset"] = forms.ItemPecasFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        forms = context["forms"]
        formset = context["formset"]
        validated = forms.is_valid()
        if not formset.is_valid() or not validated:
            return self.render_to_response(self.get_context_data(form=form))
        pecas = forms.save(commit=False)
        total = 0.00
        for price in formset.cleaned_data:
            if len(price) > 0:
                total += float(price["subtotal"].replace(",", "."))
        pecas.total = round(total, 2)
        pecas.save()
        formset.instance = pecas
        formset.save()
        return redirect("website_pecas_list")


class PecasDeleteView(DeleteView):
    success_url = reverse_lazy("website_pecas_list")
    model = models.Pecas
    template_name = "website/pecas/pecas_confirm_delete.html"


class ItensPecasDetailView(DetailView):
    model = models.Pecas
    template_name = "website/pecas/itenspecas_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ItensPecasDetailView, self).get_context_data(**kwargs)
        pecas_id = self.kwargs["pk"]
        name_pecas = context["pecas"]
        queryset = models.Itenspecas.objects.filter(pecas=name_pecas)
        context["itenspecas"] = queryset
        context["pecas_id"] = pecas_id
        context["name_pecas"] = name_pecas
        context["total"] = models.Pecas.objects.get(id=pecas_id).total
        return context


class SegmentoListView(ListView):
    template_name = "website/gasto/segmento_list.html"
    model = models.Segmento
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(SegmentoListView, self).get_context_data(**kwargs)
        # get_columns_in_the_model = [field.name for field in models.Gasto._meta.get_fields()]
        context["columns"] = [
            "parcelas_gasto",
            "id",
            "name",
            "more_infos",
            "opcoes_cartao",
            "datagasto",
            "total",
            "segmento",
        ]
        context["count"] = self.get_queryset().count()
        return context

    def get_queryset(self):
        queryset = super(SegmentoListView, self).get_queryset()

        data = self.request.GET
        if search := data.get("search"):
            RE_INT = re.compile(r"^[-+]?([1-9]\d*|0)$")
            # Essa linha qdo quero trazer o ID do gasto
            if RE_INT.match(search):
                queryset = queryset.filter(id=search)
            else:
                queryset = queryset.filter(Q(name__icontains=search))
        return queryset


class SegmentoCreateView(CreateView):
    model = models.Gasto
    template_name = "website/gasto/segmento_form.html"
    form_class = forms.SegmentoForm

    def get_context_data(self, **kwargs):
        context = super(SegmentoCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["forms"] = forms.SegmentoForm(self.request.POST)
        else:
            context["forms"] = forms.SegmentoForm()
            context["create_or_edit"] = "CADASTRAR"
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form = context["forms"]
        if not form.is_valid():
            return self.render_to_response(self.get_context_data(form=form))
        form.save()
        return redirect("website_segmento_list")


class SegmentoEditView(UpdateView):
    model = models.Segmento
    template_name = "website/gasto/segmento_form.html"
    form_class = forms.SegmentoForm

    def get_context_data(self, **kwargs):
        context = super(SegmentoEditView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["forms"] = forms.SegmentoForm(self.request.POST, instance=self.object)
        else:
            context["forms"] = forms.SegmentoForm(instance=self.object)
            context["last_data"] = models.Gasto.objects.first()
            context["create_or_edit"] = "EDITAR"
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        forms = context["forms"]
        if not forms.is_valid():
            return self.render_to_response(self.get_context_data(form=form))
        forms.save()
        return redirect("website_segmento_list")


class SegmentoDeleteView(DeleteView):
    success_url = reverse_lazy("website_segmento_list")
    model = models.Segmento
    template_name = "website/gasto/segmento_confirm_delete.html"


class GastoSegmentoListView(ListView):
    template_name = "website/gasto/gastosPorSegmento.html"
    context_object_name = "gastos"
    paginate_by = 5

    def get_queryset(self):
        queryset = super(GastoSegmentoListView, self).get_queryset()
        if search := self.request.GET.get("search"):
            RE_INT = re.compile(r"^[-+]?([1-9]\d*|0)$")
            # Essa linha qdo quero trazer o ID
            if RE_INT.match(search):
                queryset = queryset.filter(id=search)
            else:
                queryset = queryset.filter(Q(name__icontains=search))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(GastoSegmentoListView, self).get_context_data(**kwargs)
        # get_columns_in_the_model = [field.name for field in models.Gasto._meta.get_fields()]
        context["columns"] = [
            "parcelas_gasto",
            "id",
            "name",
            "more_infos",
            "opcoes_cartao",
            "datagasto",
            "total",
            "segmento",
        ]
        context["count"] = self.get_queryset().count()
        return context


# RELATÓRIO DE GASTOS POR MÊS
# ----------------------------------------------


def gastosPorMesView(request):
    template = "website/gasto/gastosPorMes.html"
    if request.method == "POST":
        context = _extracted_from_GastosPorMesView_4(request)
    else:
        segmentos = models.Segmento.objects.all()
        context = {"segmentos": segmentos}
    return render(request, template, context)


# TODO Rename this here and in `GastosPorMesView`
def _extracted_from_GastosPorMesView_4(request):
    dtInicial = request.POST.get("dtInicial")
    dtFinal = request.POST.get("dtFinal")
    today = datetime.today()
    """Se não vier com os campos date preenchidos
        será setado as datas de inicio e fim do mês corrente"""
    if dtInicial == "":
        dtInicial = datetime(today.year, today.month + 1, 1)
    if dtFinal == "":
        dtFinal = datetime(today.year, today.month + 1, today.day)
    qs = models.Gasto.objects.select_related("parcelas")
    qs = qs.exclude(name__startswith="PIX")
    qs = qs.exclude(name__startswith="TED")
    qs = qs.exclude(name__startswith="OF")
    qs = qs.filter(parcelas_gasto__data_parcela__range=[dtInicial, dtFinal])
    qs = qs.annotate(
        data_parcela=F("parcelas_gasto__data_parcela"),
        valor_parcela=F("parcelas_gasto__valor_parcela"),
        parcelas=F("parcelas_gasto__parcelas"),
        numero_parcela=F("parcelas_gasto__numero_parcela"),
    )
    qs = qs.values("id", "name", "datagasto", "data_parcela", "valor_parcela")
    qs = qs.order_by("-datagasto")
    if not qs:
        return {"dtInicial": dtInicial, "dtFinal": dtFinal}
    segmento_id = int(request.POST.get("segmento_id"))
    if segmento_id > 0:
        qs = qs.filter(segmento_id=segmento_id)
    vlr_total = sum(float(valor["valor_parcela"].replace(",", ".")) for valor in qs)

    segmentos = models.Segmento.objects.all()
    return {"data": qs, "total": vlr_total, "segmentos": segmentos}


class AutoCompleteView(FormView):
    def get(self, request):
        if q := request.GET.get("term", "").capitalize():
            gastos = models.Gasto.objects.filter(name__icontains=q)
            if gastos:
                gastos.order_by("name").distinct("name")
        else:
            gastos = models.Gasto.objects.all()
        results = []
        for gasto in gastos:
            if results:
                if gasto.name not in results[0]["name"]:
                    gasto_json = {"name": gasto.name}
                    results.append(gasto_json)
            else:
                gasto_json = {"name": gasto.name}
                results.append(gasto_json)
        data = json.dumps(results)
        mimetype = "application/json"
        return HttpResponse(data, mimetype)


def SubdividirSegmentosView(request):
    template = "website/gasto/subdividirSegmentos.html"
    segmentos = models.Segmento.objects.all()
    if request.method == "POST":
        context = _extracted_from_SubdividirSegmentosView_5(request, segmentos)
    else:
        context = {"segmentos": segmentos}
    return render(request, template, context)


# TODO Rename this here and in `SubdividirSegmentosView`
def _extracted_from_SubdividirSegmentosView_5(request, segmentos):
    dtInicial = request.POST.get("dtInicial")
    dtFinal = request.POST.get("dtFinal")
    """Se não vier com os campos date preenchidos
        será setado as datas de inicio e fim do mês corrente"""
    if dtInicial == "":
        dtInicial = datetime.now()
    else:
        # Qdo vem a data ela vem como str e precisamos paassa para o type datetime
        # já que qdo for mostrar no HTML ele espera datetime e não str
        dtInicial = datetime.strptime(dtInicial, "%Y-%m-%d")
    if dtFinal == "":
        dtFinal = add_one_month()
    else:
        # Qdo vem a data ela vem como str e precisamos paassa para o type datetime
        # já que qdo for mostrar no HTML ele espera datetime e não str
        dtFinal = datetime.strptime(dtFinal, "%Y-%m-%d")
    list_ids_segmentos = list(models.Segmento.objects.filter().values("id", "name").order_by("id"))

    dict_segmentos = {}
    for segmento in list_ids_segmentos:
        gastos_por_segmento = models.Gasto.objects.filter(
            segmento_id=segmento["id"], parcelas_gasto__data_parcela__range=[dtInicial, dtFinal]
        )
        if len(gastos_por_segmento) > 0:
            dict_segmentos[segmento["name"]] = len(gastos_por_segmento)
    nv_dict = {i: dict_segmentos[i] for i in sorted(dict_segmentos, key=dict_segmentos.get, reverse=True)}

    result = {
        "data": nv_dict,
        "segmentos": segmentos,
        "data_inicial": dtInicial,
        "data_final": dtFinal,
    }
    return result


def GastoPorParcelasView(request):
    template = "website/gasto/gastosPorParcelas.html"
    if request.method == "POST":
        context = _extracted_from_GastoPorParcelasView_4(request)
    else:
        context = {"meses": MESES}
    return render(request, template, context)


# TODO Rename this here and in `GastoPorParcelasView`
def _extracted_from_GastoPorParcelasView_4(request):
    dtInicial = request.POST.get("dtInicial")
    dtFinal = request.POST.get("dtFinal")
    porMes = request.POST.get("porMes")
    today = datetime.today()
    columns = (
        "id",
        "name",
        "parcelas",
        "numero_parcela",
        "valor_parcela",
        "data_parcela",
    )
    """Se não vier com os campos date preenchidos
        será setado as datas de inicio e fim do mês corrente"""
    if int(porMes) > 0:
        """Se mês for 1 número concatena o zero antes"""
        if len(porMes) < 2:
            porMes = "".join(("0", str(porMes)))
        dtInicial = datetime(today.year, int(porMes), 1)
        """Se o mês for FEVEREIRO vai até dia 28"""
        if today.month == 2:
            dtFinal = datetime(today.year, today.month, 28)
        else:
            dtFinal = datetime(today.year, today.month, 30)
    if dtInicial == "":
        dtInicial = datetime(today.year, today.month, 1)
    if dtFinal == "":
        """Se o mês for FEVEREIRO vai até dia 28"""
        if today.month == 2:
            dtFinal = datetime(today.year, today.month, 28)
        else:
            dtFinal = datetime(today.year, today.month, 30)
    qs = models.Gasto.objects.filter(
        parcelas_gasto__parcelas__gt=1, parcelas_gasto__data_parcela__range=[dtInicial, dtFinal]
    )
    qs = qs.annotate(
        data_parcela=F("parcelas_gasto__data_parcela"),
        valor_parcela=F("parcelas_gasto__valor_parcela"),
        parcelas=F("parcelas_gasto__parcelas"),
        numero_parcela=F("parcelas_gasto__numero_parcela"),
    )
    qs = qs.values("id", "name", "parcelas", "numero_parcela", "valor_parcela", "data_parcela")
    qs = qs.order_by("parcelas_gasto__data_parcela")
    vlr_total = sum(float(change_comma_by_dot(valor["valor_parcela"])) for valor in qs)

    return {"data": qs, "columns": columns, "total": vlr_total, "meses": MESES}


def GastoPorSegmentoView(request):
    template = "website/gasto/gastosPorSegmento.html"
    if request.method == "POST":
        context = _extracted_from_GastoPorSegmentoView_4(request)
    else:
        segmentos = models.Segmento.objects.all().order_by("id")
        context = {"segmentos": segmentos}
    return render(request, template, context)


# TODO Rename this here and in `GastoPorSegmentoView`
def _extracted_from_GastoPorSegmentoView_4(request):
    dtInicial = request.POST.get("dtInicial")
    dtFinal = request.POST.get("dtFinal")
    today = datetime.today()
    """Se não vier com os campos date preenchidos
        será setado as datas de inicio e fim do mês corrente"""
    if dtInicial == "":
        dtInicial = datetime(today.year, today.month + 1, 1)
    if dtFinal == "":
        dtFinal = datetime(today.year, today.month + 1, today.day)
    segmento_id = int(request.POST.get("segmento_id"))
    qs = models.Gasto.objects.select_related("segmento")
    qs = qs.filter(segmento_id=segmento_id, parcelas_gasto__data_parcela__range=[dtInicial, dtFinal])
    qs = qs.annotate(
        data_parcela=F("parcelas_gasto__data_parcela"),
        valor_parcela=F("parcelas_gasto__valor_parcela"),
        parcelas=F("parcelas_gasto__parcelas"),
        numero_parcela=F("parcelas_gasto__numero_parcela"),
    )
    qs = qs.values("id", "name", "datagasto", "parcelas_gasto__data_parcela", "parcelas_gasto__valor_parcela")
    qs = qs.order_by("-datagasto")
    # vlr_total = sum(
    #     float(valor["valor_parcela"].replace(",", ".")) for valor in qs
    # )
    vlr_total = 0.00

    segmentos = models.Segmento.objects.all().order_by("id")
    return {
        "data": qs,
        "total": vlr_total,
        "segmentos": segmentos,
    }


class AutoResponseView(ListView):
    ...
