# coding=utf-8

from django.contrib import admin

from .forms import PecasForm
from .models import Itenspecas, Pecas


class ItensPecasInline(admin.TabularInline):
    model = Itenspecas
    extra = 0


@admin.register(Pecas)
class PecasAdmin(admin.ModelAdmin):
    form = PecasForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "data",
                    "veiculo",
                    "proxtroca",
                    "troca",
                    "comercio",
                    "city",
                    "total",
                )
            },
        ),
    )
    inlines = (ItensPecasInline,)
    list_filter = (
        "data",
        "veiculo",
        "comercio",
        "city",
    )
    list_display = (
        "data",
        "veiculo",
        "proxtroca",
        "troca",
        "comercio",
        "city",
        "total",
    )


# @admin.register(Itenspecas)
# class ItensPecasAdmin(admin.ModelAdmin):
#     ...
