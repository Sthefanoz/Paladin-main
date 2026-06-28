from django.urls import path
from . import views

urlpatterns = [
    path(
        'CrearActivo/',
        views.crear_activo,
        name='crear_activo'
    ),

    path(
        '',
        views.lista_activos,
        name='lista_activos'
    ),

    path(
        'nuevo-ajax/',
        views.crear_activo_ajax,
        name='crear_activo_ajax'
    ),

    path(
        'editar/<int:id>/',
        views.editar_activo,
        name='editar_activo'
    ),

    path(
        'eliminar/<int:id>/',
        views.eliminar_activo,
        name='eliminar_activo'
    ),
]