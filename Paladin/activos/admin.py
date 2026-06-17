from django.contrib import admin

from .models import Activo


@admin.register(Activo)
class ActivoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre', 'tipo', 'confidencialidad', 'integridad',
        'disponibilidad', 'valor_total',
    )
    list_filter = ('tipo',)
    search_fields = ('nombre',)
