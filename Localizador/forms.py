from django import forms
from .models import Reporte, Usuario, ZonaBasura, Etiqueta, Imagen

ROLES = [
    ('admin', 'Administrador'),
    ('user', 'Usuario'),
    ('col', 'Colaborador'),
]

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        exclude = ['creador']
        widgets = {
            'fecha_reporte': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
        }

class UsuarioForm(forms.ModelForm):
    rol = forms.ChoiceField(choices=ROLES)
    fecha_registro = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    class Meta:
        model = Usuario
        fields = '__all__'


class ZonaBasuraForm(forms.ModelForm):
    fecha_registro = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    class Meta:
        model = ZonaBasura
        fields = '__all__'


# ============================
# FALTABAN ESTOS DOS FORMULARIOS
# ============================

class EtiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields = '__all__'


class ImagenForm(forms.ModelForm):
    class Meta:
        model = Imagen
        fields = '__all__'
