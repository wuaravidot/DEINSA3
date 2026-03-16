from django import forms
from .models import Pago
from datetime import date   

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['fecha_pago', 'moneda', 'monto_reportado', 'referencia_bancaria', 'comentarios']
        widgets = {
            'fecha_pago': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'max': date.today().isoformat()}),
            'moneda': forms.Select(attrs={'class': 'form-select'}),
            'monto_reportado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ej: 1500.00','min':'0.01'}),
            'referencia_bancaria': forms.TextInput(attrs={'class': 'form-control'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'moneda': 'Moneda del pago',
            'monto_reportado': 'Monto pagado',
            'referencia_bancaria': 'Nro. de Referencia',
        }
        