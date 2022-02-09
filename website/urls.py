from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .  import views as v


urlpatterns = [
    path('website/gasto/list/', v.GastoListView.as_view(), name='website_gasto_list'),
    path('website/gasto/create/', v.GastoCreateView.as_view(), name='website_gasto_create'),
    path('website/gasto/<int:pk>/edit/', v.GastoEditView.as_view(), name='website_gasto_edit'),
    path("website/gasto/<int:pk>/delete/", v.GastoDeleteView.as_view(), name="website_gasto_delete"),

    path('website/segmento/list/', v.SegmentoListView.as_view(), name='website_segmento_list'),
    path('website/segmento/create/', v.SegmentoCreateView.as_view(), name='website_segmento_create'),
    path('website/segmento/<int:pk>/edit/', v.SegmentoEditView.as_view(), name='website_segmento_edit'),
    path("website/segmento/<int:pk>/delete/", v.SegmentoDeleteView.as_view(), name="website_segmento_delete"),

    path('website/comercio/list/', v.ComercioListView.as_view(), name='website_comercio_list'),
    path('website/comercio/create/', v.ComercioCreateView.as_view(), name='website_comercio_create'),
    path('website/comercio/<int:pk>/edit/', v.ComercioEditView.as_view(), name='website_comercio_edit'),
    path("website/comercio/<int:pk>/delete/", v.ComercioDeleteView.as_view(), name="website_comercio_delete", ),

    path('website/city/list/', v.CityListView.as_view(), name='website_city_list'),
    path('website/city/create/', v.CityCreateView.as_view(), name='website_city_create'),

    path('website/pecas/list/', v.PecasListView.as_view(), name="website_pecas_list"),
    path('website/pecas/create/', v.PecasCreateView.as_view(), name="website_pecas_create"),
    path('website/pecas/<int:pk>/edit/', v.PecasEditView.as_view(), name="website_pecas_edit"),
    path("website/pecas/<int:pk>/delete/", v.PecasDeleteView.as_view(), name="website_pecas_delete", ),
    path("website/itenspecas/<int:pk>/details/", v.ItensPecasDetailView.as_view(), name="website_itenspecas_detail", ),

    path("subdividirSegmentos/", v.SubdividirSegmentosView, name="subdividirSegmentos"),
    path('gasto/autocomplete/', v.AutoCompleteView.as_view()),
    path("gastosPorParcelas/", v.GastoPorParcelasView, name="gastosPorParcelas"),
    path('gastosPorSegmento/', v.GastoPorSegmentoView, name="gastosPorSegmento"),
    path('gastosPorMes/', v.gastosPorMesView, name="gastosPorMes"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
