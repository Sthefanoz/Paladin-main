from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render, redirect
from .forms import ActivoForm

from .models import Activo

from django.shortcuts import get_object_or_404, redirect




def crear_activo(request):

    if request.method == "POST":
        form = ActivoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("lista_activos")

    else:
        form = ActivoForm()

    return render(
        request,
        "activosMain.html",
        {"form": form}
    )

def lista_activos(request):
    from django.db.models import F

    # valor_total = C + I + D, calculado en BD para ordenar/filtrar.
    activos = Activo.objects.annotate(
        valor=F('confidencialidad') + F('integridad') + F('disponibilidad')
    )

    tipo_sel = request.GET.get('tipo', '')
    orden = request.GET.get('orden', 'criticidad')  # criticidad | nombre

    if tipo_sel:
        activos = activos.filter(tipo=tipo_sel)

    if orden == 'nombre':
        activos = activos.order_by('nombre')
    else:
        activos = activos.order_by('-valor', 'nombre')

    return render(
        request,
        'lista_activos.html',
        {
            'activos': activos,
            'tipos': Activo.TIPOS_ACTIVO,
            'tipo_sel': tipo_sel,
            'orden': orden,
        }
    )

def crear_activo_ajax(request):
    """Crea un activo desde el modal del formulario de riesgo (JSON)."""
    from django.http import JsonResponse

    if request.method != "POST":
        return JsonResponse({"ok": False}, status=405)
    form = ActivoForm(request.POST)
    if form.is_valid():
        obj = form.save()
        return JsonResponse({"ok": True, "id": obj.id, "text": str(obj)})
    return JsonResponse({"ok": False, "errors": form.errors}, status=400)


def editar_activo(request, id):
    activo = get_object_or_404(Activo, id=id)
    if request.method == "POST":
        form = ActivoForm(request.POST, instance=activo)
        if form.is_valid():
            form.save()
            return redirect("lista_activos")
    else:
        form = ActivoForm(instance=activo)
    return render(request, "activosMain.html", {"form": form})


def eliminar_activo(request, id):
    activo = get_object_or_404(Activo, id=id)
    if request.method == "POST":
        activo.delete()
        return redirect('lista_activos')
    return render(request, "confirmar_eliminar_activo.html", {"activo": activo})