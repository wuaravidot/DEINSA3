from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date

class PerfilInquilino(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    numero_local = models.CharField(max_length=10)
    canon_mensual = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - Local {self.numero_local}"

class TasaCambio(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Tasas de Cambio"

    def __str__(self):
        return f"Tasa: {self.valor} ({self.fecha_actualizacion.strftime('%d/%m/%Y')})"

class Pago(models.Model):
    MONEDA_CHOICES = [
        ('BS', 'Bolívares (Bs.)'),
        ('USD', 'Dólares ($)'),
    ]
    
    inquilino = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_pago = models.DateField()

    def clean(self):
        # Validación de seguridad: No permitir fechas futuras
        if self.fecha_pago > date.today():
            raise ValidationError({'fecha_pago': "No se pueden registrar pagos con fechas posteriores a la actual."})

    def save(self, *args, **kwargs):
        self.full_clean() # Forzamos la validación antes de guardar
        super().save(*args, **kwargs)
        
    referencia_bancaria = models.CharField(max_length=50)
    moneda = models.CharField(max_length=3, choices=MONEDA_CHOICES, default='BS')
    monto_reportado = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    monto_usd = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    monto_bolivares = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    comentarios = models.TextField(blank=True, null=True)
    verificado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.inquilino.username} - {self.monto_reportado} {self.moneda}"
    