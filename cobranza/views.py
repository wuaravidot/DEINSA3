from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PerfilInquilino, Pago, TasaCambio
from .forms import PagoForm
from decimal import Decimal, ROUND_HALF_UP # IMPORTANTE PARA FINANZAS

@login_required
def dashboard_inquilino(request):
    # --- PASO 1: OBTENER PERFIL Y TASA ---
    perfil = get_object_or_404(PerfilInquilino, user=request.user)
    tasa_obj = TasaCambio.objects.latest('fecha_actualizacion')
    tasa_valor = tasa_obj.valor
    
    # --- PASO 2: CÁLCULOS DE SALDO (USD y BS) ---
    pagos = Pago.objects.filter(inquilino=request.user).order_by('-fecha_pago')
    total_pagado_usd = sum((p.monto_usd or Decimal('0.00')) for p in pagos if p.verificado)
    
    saldo_restante_usd = perfil.canon_mensual - total_pagado_usd
    # Convertimos a Decimal para el cálculo de bolívares
    saldo_restante_bs = saldo_restante_usd * Decimal(str(tasa_valor))
    
    cantidad_pendientes = pagos.filter(verificado=False).count()

    # --- PASO 3: PROCESAR EL FORMULARIO (POST) ---
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            
            # Convertimos entradas a Decimal para evitar el TypeError
            # Usamos str() para que el valor sea exacto
            monto_input = Decimal(str(pago.monto_reportado))
            tasa_dec = Decimal(str(tasa_valor))
            formato = Decimal('0.00')

            # Guardamos el monto reportado con sus dos ceros (.00)
            pago.monto_reportado = monto_input.quantize(formato)

            if pago.moneda == 'BS':
                # El usuario pagó en Bolívares
                pago.monto_bolivares = monto_input.quantize(formato)
                # Calculamos su equivalente en USD para el saldo
                pago.monto_usd = (monto_input / tasa_dec).quantize(formato, rounding=ROUND_HALF_UP)
            else:
                # El usuario pagó en Dólares
                pago.monto_usd = monto_input.quantize(formato)
                # Calculamos su equivalente en BS para el registro contable
                pago.monto_bolivares = (monto_input * tasa_dec).quantize(formato)

            # ASIGNACIÓN CORRECTA: Debe ser la instancia de User, no de Perfil
            pago.inquilino = perfil.user 
            
            pago.save()
            messages.success(request, f"Pago de {pago.monto_reportado} {pago.moneda} reportado con éxito.")
            return redirect('dashboard')
    else:
        form = PagoForm()

    # --- PASO 4: RENDERIZAR AL HTML ---
    # Nota: Usamos 'cobranza/dashboard.html' si usas subcarpetas
    return render(request, 'cobranza/dashboard.html', {
        'perfil': perfil,
        'pagos': pagos,
        'form': form,
        'tasa': tasa_valor,
        'saldo_restante_usd': max(0, saldo_restante_usd),
        'saldo_restante_bs': max(0, saldo_restante_bs),
        'cantidad_pendientes': cantidad_pendientes
    })

@login_required
def eliminar_pago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id, inquilino=request.user)
    if not pago.verificado:
        pago.delete()
        messages.warning(request, "El reporte de pago ha sido eliminado.")
    else:
        messages.error(request, "No puedes eliminar un pago que ya ha sido verificado.")
    return redirect('dashboard')