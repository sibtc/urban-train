# coding=utf-8
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, Submit, Row,
    Column, Div,
    HTML, Field
)
from cruds_adminlte import DatePickerWidget
from django import forms
from django.forms.models import inlineformset_factory
from django_select2.forms import ModelSelect2Widget

from . import models


class MyDateInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, **kwargs):
        super().__init__(format='%Y-%m-%d')


class BaseMeta:
    exclude = ('deleted', 'status')


class GastoCustomTitleWidget(ModelSelect2Widget):
    model = models.Gasto
    search_fields = [
        'name__icontains'
    ]


class ComercioCustomTitleWidget(ModelSelect2Widget):
    model = models.Comercio
    search_fields = [
        'description__icontains'
    ]


class LocalidadeCustomTitleWidget(ModelSelect2Widget):
    # model = City
    search_fields = [
        'description__icontains'
    ]


class GastoForm(forms.ModelForm):
    datagasto = forms.DateField(localize=True, widget=MyDateInput())

    class Meta(BaseMeta):
        model = models.Gasto
        widgets = {
            "datagasto": DatePickerWidget(
                attrs={"format": "dd/mm/yyyy", "icon": "fa-calendar"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(GastoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="form-group col-md-12 mb-0"),
                Column("more_infos", css_class="form-group col-md-12 mb-0"),
                Column("datagasto", css_class="form-group col-md-4 mb-0"),
                Column("segmento", css_class="form-group col-md-4 mb-0"),
                Column("opcoes_cartao", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            )
        )


class ParcelasForm(forms.ModelForm):
    data_parcela = forms.DateField(localize=True, widget=MyDateInput())

    class Meta(BaseMeta):
        model = models.Parcelas
        widgets = {
            "data_parcela": DatePickerWidget(
                attrs={"format": "dd/mm/yyyy", "icon": "fa-calendar"}
            ),
        }


ParcelasFormSet = inlineformset_factory(
    models.Gasto,
    models.Parcelas,
    form=ParcelasForm,
    extra=0,
    can_delete=True,
    fields=["parcelas", "numero_parcela", "valor_parcela", "data_parcela"],
)


class SegmentoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SegmentoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.attrs = {'novalidate': ''}

        self.helper.layout = Layout(
            Div(
                Field('name'),
            ),
        )

    class Meta(BaseMeta):
        model = models.Segmento


class PecasForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PecasForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.fields['data'].localize = True
        self.fields['data'].widget = MyDateInput()

        self.helper.layout = Layout(
            Row(
                Column('data', css_class='form-group col-md-3 mb-0'),
                Column('veiculo', css_class='form-group col-md-3 mb-0'),
                Column('proxtroca', css_class='form-group col-md-3 mb-0'),
                Column('troca', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('comercio', css_class="col-md-12"), css_class='form-row'),
        )

    class Meta(BaseMeta):
        model = models.Pecas


class ItensPecasForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ItensPecasForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Div(
                Field('description', wrapper_class="col-md-3"),
                Field('price', wrapper_class="col-md-3"),
                Field('quantity', wrapper_class="col-md-3"),
                Field('subtotal', wrapper_class="col-md-3"),
            ),
        )

    class Meta(BaseMeta):
        model = models.Itenspecas


ItemPecasFormSet = inlineformset_factory(
    models.Pecas, models.Itenspecas, form=ItensPecasForm,
    extra=0, can_delete=True
)


class ComercioForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ComercioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Field('description', wrapper_class="col-md-12"),
            )
        )

    class Meta(BaseMeta):
        model = models.Comercio


class CityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CityForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Field('description', wrapper_class="col-md-12"),
            )
        )

    class Meta(BaseMeta):
        model = models.City
