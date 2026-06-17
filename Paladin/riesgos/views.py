from django.shortcuts import render, redirect, get_object_or_404

from activos.models import Activo
from .models import Amenaza, Vulnerabilidad, Control, Riesgo
from .forms import (
    AmenazaForm, VulnerabilidadForm, ControlForm, RiesgoForm,
)


# ---------------------------------------------------------------------------
# Riesgos (CRUD) — módulos: identificación, valoración, tratamiento, residual
# ---------------------------------------------------------------------------

def lista_riesgos(request):
    riesgos = (
        Riesgo.objects
        .select_related('activo', 'amenaza', 'vulnerabilidad')
        .all()
    )
    return render(request, 'riesgos/lista_riesgos.html', {'riesgos': riesgos})


def crear_riesgo(request):
    form = RiesgoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('lista_riesgos')
    return render(
        request, 'riesgos/form_riesgo.html',
        {'form': form, 'titulo': 'Registrar Riesgo'}
    )


def editar_riesgo(request, id):
    riesgo = get_object_or_404(Riesgo, id=id)
    form = RiesgoForm(request.POST or None, instance=riesgo)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('lista_riesgos')
    return render(
        request, 'riesgos/form_riesgo.html',
        {'form': form, 'titulo': 'Editar Riesgo'}
    )


def detalle_riesgo(request, id):
    riesgo = get_object_or_404(
        Riesgo.objects.select_related('activo', 'amenaza', 'vulnerabilidad'),
        id=id,
    )
    return render(request, 'riesgos/detalle_riesgo.html', {'riesgo': riesgo})


def eliminar_riesgo(request, id):
    riesgo = get_object_or_404(Riesgo, id=id)
    if request.method == 'POST':
        riesgo.delete()
        return redirect('lista_riesgos')
    return render(request, 'riesgos/confirmar_eliminar.html',
                  {'objeto': riesgo, 'volver': 'lista_riesgos'})


# ---------------------------------------------------------------------------
# Catálogos: Amenazas, Vulnerabilidades, Controles
# ---------------------------------------------------------------------------

def lista_amenazas(request):
    return render(request, 'riesgos/lista_amenazas.html',
                  {'amenazas': Amenaza.objects.all()})


def crear_amenaza(request):
    form = AmenazaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('lista_amenazas')
    return render(request, 'riesgos/form_simple.html',
                  {'form': form, 'titulo': 'Registrar Amenaza',
                   'volver': 'lista_amenazas'})


def lista_vulnerabilidades(request):
    return render(request, 'riesgos/lista_vulnerabilidades.html',
                  {'vulnerabilidades': Vulnerabilidad.objects.all()})


def crear_vulnerabilidad(request):
    form = VulnerabilidadForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('lista_vulnerabilidades')
    return render(request, 'riesgos/form_simple.html',
                  {'form': form, 'titulo': 'Registrar Vulnerabilidad',
                   'volver': 'lista_vulnerabilidades'})


def lista_controles(request):
    return render(request, 'riesgos/lista_controles.html',
                  {'controles': Control.objects.all()})


def crear_control(request):
    form = ControlForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('lista_controles')
    return render(request, 'riesgos/form_simple.html',
                  {'form': form, 'titulo': 'Registrar Control',
                   'volver': 'lista_controles'})


# ---------------------------------------------------------------------------
# Monitoreo y supervisión (panel) + Comunicación (reporte)
# ---------------------------------------------------------------------------

def _resumen_riesgos():
    """Construye las métricas que comparten el dashboard y el reporte."""
    riesgos = list(
        Riesgo.objects
        .select_related('activo', 'amenaza', 'vulnerabilidad')
        .all()
    )

    por_estado = {clave: 0 for clave, _ in Riesgo.ESTADOS}
    por_nivel = {'Bajo': 0, 'Medio': 0, 'Alto': 0, 'Crítico': 0}

    for r in riesgos:
        por_estado[r.estado] = por_estado.get(r.estado, 0) + 1
        por_nivel[r.nivel_riesgo_texto] = por_nivel.get(r.nivel_riesgo_texto, 0) + 1

    # Etiquetas legibles para los estados.
    etiquetas_estado = dict(Riesgo.ESTADOS)
    estados = [
        {'nombre': etiquetas_estado[k], 'total': v}
        for k, v in por_estado.items()
    ]

    # Riesgos prioritarios: mayor nivel inherente primero.
    criticos = sorted(riesgos, key=lambda r: r.nivel_riesgo, reverse=True)[:10]

    return {
        'total': len(riesgos),
        'estados': estados,
        'niveles': por_nivel,
        'criticos': criticos,
        'riesgos': riesgos,
    }


def dashboard(request):
    contexto = _resumen_riesgos()
    contexto['total_activos'] = Activo.objects.count()
    return render(request, 'riesgos/dashboard.html', contexto)


def reporte(request):
    """Reporte para partes interesadas (comunicación y consulta)."""
    contexto = _resumen_riesgos()
    return render(request, 'riesgos/reporte.html', contexto)
