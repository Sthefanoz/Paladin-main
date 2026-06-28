import re

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
            'cve': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'CVE-AAAA-NNNN'}
            ),
        }

    def clean_cve(self):
        """Valida el formato del identificador CVE (CVE-AAAA-NNNN)."""
        cve = (self.cleaned_data.get('cve') or '').strip().upper()
        if cve and not re.fullmatch(r'CVE-\d{4}-\d{4,7}', cve):
            raise forms.ValidationError(
                'Formato CVE inválido. Use el formato CVE-AAAA-NNNN '
                '(por ejemplo, CVE-2021-44228).'
            )
        return cve


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
            'fecha_tratamiento', 'fecha_control',
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
            'fecha_tratamiento': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'fecha_control': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
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

        # Coherencia de fechas y estado de monitoreo.
        f_trat = cleaned.get('fecha_tratamiento')
        f_ctrl = cleaned.get('fecha_control')
        if f_trat and f_ctrl and f_ctrl < f_trat:
            self.add_error(
                'fecha_control',
                'La fecha de control no puede ser anterior a la del tratamiento.'
            )

        estado = cleaned.get('estado')
        # Para marcar como "Controlado" debe registrarse la fecha de control.
        if estado == 'CON' and not f_ctrl:
            self.add_error(
                'fecha_control',
                'Para marcar el riesgo como "Controlado" indique la fecha de control.'
            )
        # No se puede controlar un riesgo que aún no fue tratado.
        if f_ctrl and not f_trat:
            self.add_error(
                'fecha_tratamiento',
                'Registre primero la fecha del tratamiento antes de la de control.'
            )

        return cleaned
