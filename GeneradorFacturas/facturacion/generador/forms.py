# generador/forms.py

from django import forms
from .models import Factura

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['cantidad', 'fecha', 'correo', 'rfc', 'otros_datos']
