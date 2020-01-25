from .views import (
    GastoSegmentoListView, gastosPorMesView, AutoCompleteView,
    SegmentoCRUD, GastoCRUD, HoraTrabalhadaCRUD, RabbiitCRUD,
    CityCRUD, PecasCRUD, ComercioCRUD, guiaBolsoView
)

from django.urls import path, include

segmento_view = SegmentoCRUD()
rabbiit_view = RabbiitCRUD()
gasto_view = GastoCRUD()
horatrabalhada_view = HoraTrabalhadaCRUD()
localidade_view = CityCRUD()
pecas_view = PecasCRUD()
comercio_view = ComercioCRUD()

urlpatterns = [
    path('', include(segmento_view.get_urls())),
    path('', include(rabbiit_view.get_urls())),
    path('', include(gasto_view.get_urls())),
    path('', include(horatrabalhada_view.get_urls())),
    path('', include(localidade_view.get_urls())),
    path('', include(pecas_view.get_urls())),
    path('', include(comercio_view.get_urls())),
    path('gasto/autocomplete/', AutoCompleteView.as_view()),
    path('gastosPorSegmento/', GastoSegmentoListView.as_view(), name="gastosPorSegmento"),
    path('gastosPorMes/', gastosPorMesView, name="gastosPorMes"),
    path('guiaBolso/', guiaBolsoView, name="guiaBolso"),
    path('select2/', include('django_select2.urls')),
]
