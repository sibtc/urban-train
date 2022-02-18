from django.urls import reverse

import pytest

from urban_train.django_assertions import assert_contains
from website.models import Comercio


@pytest.fixture
def resp(client, db):
    return client.get(reverse("website_gasto_list"))


def test_status_code(resp):
    assert resp.status_code == 200


def test_title(resp):
    assert_contains(resp, "<title>Lista de Gastos</title>")


# def create_gasto():
#
#     assert 1 == 1


@pytest.mark.parametrize(
    "comercios",
    [
        [Comercio(description="Supermercado Nagai"), Comercio(description="Podologia")],
        [Comercio(description="Oficina do Alemão")],
    ],
)
def test_record_comercio(sessao, comercios):
    for comercio in comercios:
        sessao.salvar(comercio)
