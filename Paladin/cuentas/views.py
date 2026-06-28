from django.contrib.auth import login
from django.contrib.auth.decorators import login_not_required
from django.shortcuts import render, redirect

from .forms import RegistroForm


@login_not_required
def registro(request):
    """Registra un nuevo usuario y lo inicia sesión automáticamente."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = RegistroForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')

    return render(request, 'cuentas/registro.html', {'form': form})
