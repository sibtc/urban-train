# coding=utf-8
from django.db import models
from django.urls import reverse
from django_pandas.managers import DataFrameManager
from django.utils.translation import gettext as _
from accounts.models import Base
from .constants import TYPE_VEHICLE
from django.db.models.signals import post_save
from django.dispatch import receiver
from utils import change_comma_by_dot



class Segmento(Base):

    name = models.CharField('Tipo de comércio', max_length=100)
    slug = models.SlugField('Identificador', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Segmento do Comercio'
        verbose_name_plural = 'Segmentos do Comercio'
        ordering = ['id']

    # Serve para quando buscar um comércio trazer os gastos do mesmo
    def get_absolute_url(self):
        return reverse(
            'website:gastosPorSegmento',
        )

    objects = DataFrameManager()


class Gasto(Base):

    name = models.CharField(max_length=100, verbose_name=("nome"))
    slug = models.SlugField('Identificador', max_length=100)
    parcelas = models.IntegerField(default=1)
    valor = models.CharField(max_length=100)
    datagasto = models.DateField()
    segmento = models.ForeignKey(Segmento, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'
        ordering = ['-id']

    objects = DataFrameManager()


class HoraTrabalhada(Base):
    price = models.CharField(max_length=100, verbose_name='Ganho/hora', default=0)

    def __str__(self):
        return self.price

    def __repr__(self):
        return str(self.price)

    class Meta:
        verbose_name_plural = 'Horas Trabalhadas'
        ordering = ['-id']


class Rabbiit(Base):

    description = models.CharField(verbose_name="Descrição", max_length=100)
    time_total = models.TimeField(verbose_name='Total de horas', blank=True, null=True)
    time_start = models.TimeField(verbose_name='Hora Inicial', blank=True, null=True)
    time_end = models.TimeField(verbose_name='Hora Final', blank=True, null=True)
    rate_hour = models.ForeignKey(HoraTrabalhada,
                                verbose_name='Ganho/hora',
                                on_delete=models.SET_NULL,
                                null=True, blank=True)
    rate_total = models.DecimalField(verbose_name='Total Ganho', max_digits=6, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.description

    def __repr__(self):
        return str(self.description)

    class Meta:
        verbose_name_plural = 'Rabbiits'
        ordering = ['-id']

    objects = DataFrameManager()


class City(Base):

    description = models.CharField(verbose_name=_('Description'), max_length=100)

    def __str__(self):
        return self.description

    def __repr__(self):
        return str(self.description)

    class Meta:
        verbose_name = 'Localidade'
        verbose_name_plural = 'Localidades'
        ordering = ['-id']


class Comercio(Base):

    description = models.CharField(
        verbose_name=_('Descrição'),
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.description

    # def __repr__(self):
    #     return str(self.description)

    class Meta:
        verbose_name = 'Comércio'
        verbose_name_plural = 'Comércios'
        ordering = ['-id']


class Pecas(Base):

    data = models.DateField()
    veiculo = models.CharField(verbose_name=_('Veículo'), choices=TYPE_VEHICLE, max_length=1)
    proxtroca = models.IntegerField(default=1)
    troca = models.IntegerField(default=1)
    comercio = models.ForeignKey(Comercio, verbose_name='Comércio', on_delete=models.PROTECT)
    city = models.ForeignKey(City, verbose_name='Localidade', on_delete=models.PROTECT)
    total = models.CharField(verbose_name='Total', blank=True, null=True, max_length=100)

    def __str__(self):
        return self.comercio.description

    # def __repr__(self):
    #     return str(self.comercio.description)

    class Meta:
        verbose_name = 'Peça'
        verbose_name_plural = 'Peças'
        ordering = ['id']

    # objects = DataFrameManager()


class Itenspecas(models.Model):

    description = models.CharField(verbose_name='Descrição', max_length=100)
    pecas = models.ForeignKey(Pecas, verbose_name='Peças', on_delete=models.PROTECT)
    price = models.CharField(verbose_name='Preço', blank=True, null=True, max_length=100)
    quantity = models.IntegerField(verbose_name='Quantidade Comprada', default=1)
    subtotal = models.CharField(verbose_name='Sub-Total', blank=True, null=True, max_length=100)


    def __str__(self):
        return self.description


    def __repr__(self):
        return str(self.description)


    class Meta:
        verbose_name = 'Item Peça'
        verbose_name_plural = 'Itens Peças'
        ordering = ['-id']


@receiver(post_save, sender=Itenspecas)
def PecasPosSave(instance, sender, created=False, **kwargs):
    pecas = Pecas.objects.filter(id=instance.pecas_id)
    price = float(change_comma_by_dot(instance.price))
    qt = instance.quantity
    try:
        total = float(list(pecas)[0].total)
    except:
        total = 0.00
    pcs = Pecas()
    pcs.id = instance.pecas_id
    if created:
        try:
            pcs.total = price * qt + total
        except Exception as err:
            print(err)
            pcs.total = price * qt

    pcs.save(update_fields=['total'])


