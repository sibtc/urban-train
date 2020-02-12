# coding=utf-8
from .models import (
    Segmento, Gasto, Rabbiit, HoraTrabalhada,
    Pecas, Comercio, Itenspecas, City
)
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, Submit, Row,
    Column, Button, Div,
    HTML, Field
)
from crispy_forms.bootstrap import InlineField, FormActions
import datetime
from django_select2.forms import ModelSelect2Widget
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.forms.models import inlineformset_factory


class MyDateInput(forms.DateInput):
    input_type = 'date'
    def __init__(self, **kwargs):
        super().__init__(format='%Y-%m-%d')


class BaseMeta:
    exclude = ('deleted', 'status')


def due_time():
    return datetime.time()


class GastoCustomTitleWidget(ModelSelect2Widget):
    model = Gasto
    search_fields = [
        'name__icontains'
    ]

    def label_from_instance(self, obj):
        return force_text(obj.name).upper()

class SegmentoCustomTitleWidget(ModelSelect2Widget):
    model = Segmento
    search_fields = [
        'name__icontains'
    ]

    def label_from_instance(self, obj):
        return force_text(obj.name).upper()


class ComercioCustomTitleWidget(ModelSelect2Widget):
    model = Comercio
    search_fields = [
        'description__icontains'
    ]

    def label_from_instance(self, obj):
        return force_text(obj.description).upper()

class LocalidadeCustomTitleWidget(ModelSelect2Widget):
    model = City
    search_fields = [
        'description__icontains'
    ]

    def label_from_instance(self, obj):
        return force_text(obj.description).upper()


class GastoForm(forms.ModelForm):

    datagasto = forms.DateField(localize=True, widget=MyDateInput())

    class Meta(BaseMeta):
        model = Gasto
        fields = ['name', 'slug', 'valor', 'datagasto', 'segmento', 'parcelas']
        widgets = {
            # 'name': GastoCustomTitleWidget,
            'segmento': SegmentoCustomTitleWidget,
        }

    def __init__(self, *args, **kwargs):
        super(GastoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'name',
            'slug',
            Row(
                Column('valor', css_class='form-group col-md-6 mb-0'),
                Column('datagasto', css_class='form-group col-md-6 mb-0'),
                Column('segmento', css_class='form-group col-md-6 mb-0'),
                Column('parcelas', css_class='form-group col-md-6 mb-0'),
            ),
            Div(
                FormActions(
                    Submit('submit', _('Submit'), css_class='btn btn-primary'),
                    HTML("""{% load i18n %}<a class="btn btn-danger"
                        href="{{ url_delete }}">{% trans 'Delete' %}</a>"""),
                    css_class="col-md-12"
                )
            )
        )


class SegmentoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SegmentoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.attrs = {'novalidate': ''}

        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('slug', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', _('Submit'),),
        )

    class Meta(BaseMeta):
        model = Segmento


class RabbiitForm(forms.ModelForm):

    class Meta(BaseMeta):
        model = Rabbiit
        fields = ['description', 'rate_hour',
                  'time_end', 'time_start',
                  'time_total', 'rate_total',
                  ]

    def __init__(self, *args, **kwargs):
        super(RabbiitForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.fields['time_start'].widget = forms.HiddenInput()
        self.fields['time_end'].widget = forms.HiddenInput()
        self.fields['time_total'].widget = forms.HiddenInput()

        self.helper.layout = Layout(
            'description',
            'rate_hour',
            'time_end',
            'time_start',
            'time_total',
            Div(
                Button('start_timer',
                       'Start',
                       css_id='start_timer',
                       css_class='btn btn-primary',
                       onclick=''
               ),
                Button('end_timer',
                       'Stop',
                       css_id='end_timer',
                       css_class='btn btn-success'
               ),
            ),
            InlineField(
                Div(
                    HTML("<span class='show-time' id='show_time_initial'></span>"),
                    HTML("<span class='show-time' id='show_time'></span>"),
                    HTML("<span class='show-time' id='show_time_result'></span>"),
                ),
            ),
            Div(
                Submit('submit', ('Enviar'),),
            )
        )

    def save(self, commit=True):
        o = super(RabbiitForm, self).save(commit=False)
        t_tempo = self.cleaned_data['time_total'].minute
        price = float(self.cleaned_data['rate_hour'].price.replace(',', '.'))
        result = t_tempo / 60 * price
        self.instance.rate_total = result
        if commit:
            o.save()
        return o


class HoraTrabalhadaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(HoraTrabalhadaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            'price',
            'created_at',
            'modified_at',
            Submit('submit', ('Enviar'),),
        )

    class Meta(BaseMeta):
        model = HoraTrabalhada


class PecasForm(forms.ModelForm):

    # total = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

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
            Div(
                Field('comercio', wrapper_class="col-md-12"),
            ),
            Row(
                Column('city', css_class='form-group col-md-6 mb-0'),
                Column('total', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            )
        )

    class Meta(BaseMeta):
        model = Pecas
        widgets = {'comercio': ComercioCustomTitleWidget,
                   'city': LocalidadeCustomTitleWidget,
        }


class ItensPecasForm(forms.ModelForm):

    subtotal = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

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
            Div(
                FormActions(
                    Submit('submit', _('Submit'), css_class='btn btn-primary'),
                    HTML("""{% load i18n %}
                                {% if url_delete %}
                                <a class="btn btn-danger"
                                  href="{{ url_delete }}">{% trans 'Excluir' %}</a>
                                {% endif %}  
                                  """),
                    css_class="col-md-3"
                )
            )
        )

    class Meta(BaseMeta):
        model = Itenspecas

ItemPecasFormSet = inlineformset_factory(
    Pecas, Itenspecas, form=ItensPecasForm,
    extra=0, can_delete=True
)

class ComercioForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ComercioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Div(
                Field('description', wrapper_class="col-md-12"),
            ),
            Div(
                FormActions(
                    Submit('submit', _('Enviar'), css_class='btn btn-primary'),
                    HTML("""{% load i18n %}
                                        {% if url_delete %}
                                        <a class="btn btn-danger"
                                          href="{{ url_delete }}">{% trans 'Delete' %}</a>
                                        {% endif %}  
                                          """),
                    css_class="col-md-12"
                )
            )
        )

    class Meta(BaseMeta):
        model = Comercio

ItemPecasFormSet = inlineformset_factory(
    Pecas, Itenspecas, form=ItensPecasForm,
    fields=['description', 'pecas', 'price', 'quantity', 'subtotal'],
    extra=1, can_delete=True
)
