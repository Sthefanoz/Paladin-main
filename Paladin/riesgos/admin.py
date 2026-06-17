from django.contrib import admin

from .models import Amenaza, Vulnerabilidad, Control, Riesgo


@admin.register(Amenaza)
class AmenazaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nombre',)


@admin.register(Vulnerabilidad)
class VulnerabilidadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Control)
class ControlAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'tema')
    list_filter = ('tema',)
    search_fields = ('codigo', 'nombre')


@admin.register(Riesgo)
class RiesgoAdmin(admin.ModelAdmin):
    list_display = (
        'activo', 'amenaza', 'probabilidad', 'impacto',
        'nivel_riesgo', 'nivel_riesgo_texto', 'estado',
    )
    list_filter = ('estado', 'estrategia')
    search_fields = ('activo__nombre', 'amenaza__nombre')
    filter_horizontal = ('controles_propuestos',)
