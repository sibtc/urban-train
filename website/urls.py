from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .views import (
    GastoSegmentoListView, gastosPorMesView, AutoCompleteView,
    SegmentoCRUD, GastoCRUD, RabbiitCRUD,
    CityCRUD, ComercioCRUD, PecasListView,
    PecasCreateView, PecasEditView, HoraTrabalhadaListView,
    HoraTrabalhadaCreateView, HoraTrabalhadaEditView,
    HoraTrabalhadaDeleteView
)

segmento_view = SegmentoCRUD()
rabbiit_view = RabbiitCRUD()
gasto_view = GastoCRUD()
localidade_view = CityCRUD()
comercio_view = ComercioCRUD()

urlpatterns = [
    path('', include(segmento_view.get_urls())),
    path('', include(rabbiit_view.get_urls())),
    path('', include(gasto_view.get_urls())),
    path('', include(localidade_view.get_urls())),
    path('website/horatrabalhada/list/', HoraTrabalhadaListView.as_view(), name="website_horatrabalhada_list"),
    path('website/horatrabalhada/create/', HoraTrabalhadaCreateView.as_view(), name="website_horatrabalhada_create"),
    path('website/horatrabalhada/edit/<pk>/', HoraTrabalhadaEditView.as_view(), name="website_horatrabalhada_edit"),
    path('website/horatrabalhada/delete/<pk>/', HoraTrabalhadaDeleteView.as_view(),
         name="website_horatrabalhada_delete"),
    path('website/pecas/list/', PecasListView.as_view(), name="website_pecas_list"),
    path('website/pecas/create/', PecasCreateView.as_view(), name="website_pecas_create"),
    path('website/pecas/edit/<pk>/', PecasEditView.as_view(), name="website_pecas_edit"),
    path('', include(comercio_view.get_urls())),
    path('gasto/autocomplete/', AutoCompleteView.as_view()),
    path('gastosPorSegmento/', GastoSegmentoListView.as_view(), name="gastosPorSegmento"),
    path('gastosPorMes/', gastosPorMesView, name="gastosPorMes"),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    # if "debug_toolbar" in settings.INSTALLED_APPS:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
