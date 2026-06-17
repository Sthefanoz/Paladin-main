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

    activos = Activo.objects.all()

    return render(
        request,
        'lista_activos.html',
        {
            'activos': activos
        }
    )

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