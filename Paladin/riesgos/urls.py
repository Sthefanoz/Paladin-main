from django.urls import path
from . import views

urlpatterns = [
    # Panel principal de monitoreo
    path('', views.dashboard, name='dashboard'),
    path('reporte/', views.reporte, name='reporte'),
    path('reporte/excel/', views.reporte_excel, name='reporte_excel'),

    # Riesgos
    path('riesgos/', views.lista_riesgos, name='lista_riesgos'),
    path('riesgos/nuevo/', views.crear_riesgo, name='crear_riesgo'),
    path('riesgos/<int:id>/', views.detalle_riesgo, name='detalle_riesgo'),
    path('riesgos/<int:id>/editar/', views.editar_riesgo, name='editar_riesgo'),
    path('riesgos/<int:id>/eliminar/', views.eliminar_riesgo, name='eliminar_riesgo'),

    # Amenazas
    path('amenazas/', views.lista_amenazas, name='lista_amenazas'),
    path('amenazas/nueva/', views.crear_amenaza, name='crear_amenaza'),
    path('amenazas/nueva-ajax/', views.crear_amenaza_ajax, name='crear_amenaza_ajax'),
    path('amenazas/<int:id>/eliminar/', views.eliminar_amenaza, name='eliminar_amenaza'),

    # Vulnerabilidades
    path('vulnerabilidades/', views.lista_vulnerabilidades, name='lista_vulnerabilidades'),
    path('vulnerabilidades/nueva/', views.crear_vulnerabilidad, name='crear_vulnerabilidad'),
    path('vulnerabilidades/nueva-ajax/', views.crear_vulnerabilidad_ajax, name='crear_vulnerabilidad_ajax'),
    path('vulnerabilidades/<int:id>/eliminar/', views.eliminar_vulnerabilidad, name='eliminar_vulnerabilidad'),

    # Controles ISO 27002:2022
    path('controles/', views.lista_controles, name='lista_controles'),
    path('controles/nuevo/', views.crear_control, name='crear_control'),
    path('controles/<int:id>/eliminar/', views.eliminar_control, name='eliminar_control'),
]
