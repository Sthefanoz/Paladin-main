from django import forms
from .models import Activo

class ActivoForm(forms.ModelForm):

    class Meta:
        model = Activo
        fields = '__all__'

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'confidencialidad': forms.Select(attrs={'class': 'form-select'}),
            'integridad': forms.Select(attrs={'class': 'form-select'}),
            'disponibilidad': forms.Select(attrs={'class': 'form-select'}),
        }