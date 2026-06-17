from django import forms

from .models import Amenaza, Vulnerabilidad, Control, Riesgo


_TEXT = {'class': 'form-control'}
_AREA = {'class': 'form-control', 'rows': 3}
_SELECT = {'class': 'form-select'}


class AmenazaForm(forms.ModelForm):
    class Meta:
        model = Amenaza
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs=_TEXT),
            'descripcion': forms.Textarea(attrs=_AREA),
            'categoria': forms.Select(attrs=_SELECT),
        }


class VulnerabilidadForm(forms.ModelForm):
    class Meta:
        model = Vulnerabilidad
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs=_TEXT),
            'descripcion': forms.Textarea(attrs=_AREA),
        }


class ControlForm(forms.ModelForm):
    class Meta:
        model = Control
        fields = '__all__'
        widgets = {
            'codigo': forms.TextInput(attrs=_TEXT),
            'nombre': forms.TextInput(attrs=_TEXT),
            'tema': forms.Select(attrs=_SELECT),
            'descripcion': forms.Textarea(attrs=_AREA),
        }


class RiesgoForm(forms.ModelForm):
    class Meta:
        model = Riesgo
        fields = [
            'activo', 'amenaza', 'vulnerabilidad', 'controles_existentes',
            'probabilidad', 'impacto',
            'estrategia', 'controles_propuestos', 'responsable',
            'probabilidad_residual', 'impacto_residual',
            'observaciones', 'estado',
        ]
        widgets = {
            'activo': forms.Select(attrs=_SELECT),
            'amenaza': forms.Select(attrs=_SELECT),
            'vulnerabilidad': forms.Select(attrs=_SELECT),
            'controles_existentes': forms.Textarea(attrs=_AREA),
            'probabilidad': forms.Select(attrs=_SELECT),
            'impacto': forms.Select(attrs=_SELECT),
            'estrategia': forms.Select(attrs=_SELECT),
            'controles_propuestos': forms.SelectMultiple(
                attrs={'class': 'form-select', 'size': 8}
            ),
            'responsable': forms.TextInput(attrs=_TEXT),
            'probabilidad_residual': forms.Select(attrs=_SELECT),
            'impacto_residual': forms.Select(attrs=_SELECT),
            'observaciones': forms.Textarea(attrs=_AREA),
            'estado': forms.Select(attrs=_SELECT),
        }

    def clean(self):
        """Validación de datos de entrada (exigida por la consigna)."""
        cleaned = super().clean()

        prob_res = cleaned.get('probabilidad_residual')
        imp_res = cleaned.get('impacto_residual')

        # El riesgo residual debe definir ambos valores o ninguno.
        if bool(prob_res) ^ bool(imp_res):
            raise forms.ValidationError(
                'Para el riesgo residual debe indicar tanto la probabilidad '
                'como el impacto residual (o dejar ambos vacíos).'
            )

        # El riesgo residual no puede ser mayor que el inherente.
        prob = cleaned.get('probabilidad')
        imp = cleaned.get('impacto')
        if prob and imp and prob_res and imp_res:
            if (prob_res * imp_res) > (prob * imp):
                raise forms.ValidationError(
                    'El riesgo residual no puede ser mayor que el riesgo '
                    'inherente: los controles no deberían aumentar el riesgo.'
                )

        # Si se eligió "Mitigar", debe registrarse al menos un control propuesto.
        estrategia = cleaned.get('estrategia')
        controles = cleaned.get('controles_propuestos')
        if estrategia == 'MIT' and not controles:
            self.add_error(
                'controles_propuestos',
                'Si la estrategia es "Mitigar" debe seleccionar al menos un control.'
            )

        return cleaned
