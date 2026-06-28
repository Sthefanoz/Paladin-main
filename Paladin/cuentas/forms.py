from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistroForm(UserCreationForm):
    """Formulario de registro con campos estilizados (Bootstrap) y en español."""

    email = forms.EmailField(
        required=True,
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Usuario',
        }
        help_texts = {
            'username': 'Obligatorio. Máximo 150 caracteres. Solo letras, '
                        'dígitos y @/./+/-/_.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Etiquetas y textos de ayuda en español para las contraseñas.
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'
        self.fields['password1'].help_text = (
            'Mínimo 8 caracteres. No puede ser solo números, ni una contraseña '
            'común, ni parecerse a tus datos personales.'
        )
        self.fields['password2'].help_text = (
            'Escribe la misma contraseña otra vez, para verificarla.'
        )
        # Aplica la clase Bootstrap a todos los campos.
        for campo in self.fields.values():
            campo.widget.attrs.setdefault('class', 'form-control')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe una cuenta con este correo.')
        return email
