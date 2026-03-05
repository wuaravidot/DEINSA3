from django.contrib import admin
from .models import PerfilInquilino, Pago, TasaCambio

@admin.register(PerfilInquilino)
class InquilinoAdmin(admin.ModelAdmin):
    # Eliminamos 'fecha_proximo_aumento' que causaba el error
    list_display = ('user', 'numero_local', 'canon_mensual')
    search_fields = ('user__username', 'numero_local')

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    # Añadimos 'moneda' y 'verificado' para que puedas gestionar los abonos
    list_display = ('inquilino', 'fecha_pago', 'monto_reportado', 'moneda', 'monto_usd', 'verificado')
    list_filter = ('verificado', 'moneda', 'fecha_pago')
    # Esto te permite marcar como verificado directamente desde la lista
    list_editable = ('verificado',) 

@admin.register(TasaCambio)
class TasaCambioAdmin(admin.ModelAdmin):
    list_display = ('valor', 'fecha_actualizacion')