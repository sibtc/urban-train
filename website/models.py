# coding=utf-8
from django.db import models
from django.utils.translation import gettext as _

# from .constants import TYPE_VEHICLE
from accounts import constants
from accounts.models import Base


class Segmento(Base):
    name = models.CharField("Tipo de segmento", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Segmento do Comercio"
        verbose_name_plural = "Segmentos do Comercio"
        ordering = ["id"]


class Gasto(Base):
    name = models.CharField(max_length=100, verbose_name=("nome"))
    more_infos = models.CharField(verbose_name=("Infos Complementares"), max_length=100, null=True, blank=True)
    opcoes_cartao = models.CharField(
        verbose_name=("Tipo de pagamento"),
        max_length=1,
        choices=constants.CARTAO,
        default=constants.CREDITO,
    )
    datagasto = models.DateField(verbose_name=_("Date Spent"))
    total = models.CharField("Valor Total", max_length=100, null=True, blank=True)
    segmento = models.ForeignKey(Segmento, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"
        ordering = ["-id"]


class Parcelas(models.Model):
    gasto = models.ForeignKey(Gasto, related_name="parcelas_gasto", on_delete=models.CASCADE)
    parcelas = models.IntegerField("Total de parcelas", default=1)
    numero_parcela = models.IntegerField("Número da parcela", default=1)
    valor_parcela = models.CharField("Valor da Parcela", max_length=100, blank=True, null=True)
    data_parcela = models.DateField(verbose_name=_("Installment Date"), blank=True, null=True)

    class Meta:
        verbose_name = "Parcela do gasto"
        verbose_name_plural = "Parcelas dos gasto"

    def __repr__(self):
        return self.gasto.name

    def __str__(self):
        return f"Total de parcelas..: {self.parcelas}"


class City(Base):
    description = models.CharField(verbose_name="Localidade", max_length=100)

    def __str__(self):
        return self.description

    def __repr__(self):
        return str(self.description)

    class Meta:
        verbose_name = "Localidade"
        verbose_name_plural = "Localidades"
        ordering = ["-id"]


class Comercio(Base):
    description = models.CharField(verbose_name=_("Descrição"), max_length=100, unique=True)

    def __str__(self):
        return self.description

    def __repr__(self):
        return str(self.description)

    class Meta:
        verbose_name = "Comércio"
        verbose_name_plural = "Comércios"
        ordering = ["-id"]


class Pecas(Base):
    data = models.DateField(
        verbose_name=_("Data"),
    )
    veiculo = models.CharField(verbose_name=_("Veículo"), choices=constants.TYPE_VEHICLE, max_length=1)
    proxtroca = models.IntegerField(verbose_name=_("Próxima Troca"), default=1)
    troca = models.IntegerField(verbose_name=_("Troca"), default=1)
    comercio = models.ForeignKey(Comercio, verbose_name=_("Comércio"), on_delete=models.PROTECT)
    city = models.ForeignKey(City, verbose_name="Localidade", on_delete=models.PROTECT, null=True, blank=True)
    total = models.CharField(verbose_name=_("Total"), blank=True, null=True, max_length=100)

    def __str__(self):
        return self.comercio.description

    class Meta:
        verbose_name = _("Peça")
        verbose_name_plural = _("Peças")
        ordering = ["id"]


class Itenspecas(models.Model):
    description = models.CharField(verbose_name="Descrição", max_length=100)
    pecas = models.ForeignKey(Pecas, verbose_name="Peças", on_delete=models.PROTECT)
    price = models.CharField(verbose_name="Preço", blank=True, null=True, max_length=100)
    quantity = models.IntegerField(verbose_name="Quantidade Comprada", default=1)
    subtotal = models.CharField(verbose_name="Sub-Total", blank=True, null=True, max_length=100)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Item Peça"
        verbose_name_plural = "Itens Peças"
        ordering = ["-id"]
