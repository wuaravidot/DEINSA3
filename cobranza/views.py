from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PerfilInquilino, Pago, TasaCambio
from .forms import PagoForm
from django.db.models import Sum

@login_required
def dashboard_inquilino(request):
    # --- PASO 0: DISTINCIÓN DE USUARIOS ---
    # Si el usuario es administrador (Staff), lo mandamos al panel azul
    if request.user.is_staff:
        return redirect('/admin/')

    # Intentamos obtener el perfil del inquilino
    try:
        perfil = PerfilInquilino.objects.get(user=request.user)
    except PerfilInquilino.DoesNotExist:
        # Si no es admin pero no tiene perfil, lo mandamos al login por seguridad
        return redirect('/accounts/login/')

    # --- TU CÓDIGO DE CÁLCULOS (PASOS 1, 2 y 3) ---
    
    # 1. Obtener Tasa de Cambio
    try:
        tasa_obj = TasaCambio.objects.latest('fecha_actualizacion')
        tasa_valor = float(tasa_obj.valor)
    except TasaCambio.DoesNotExist:
        tasa_valor = 1.0

    # 2. Historial de Pagos y Notificaciones (Círculo Amarillo)
    pagos = Pago.objects.filter(inquilino=request.user).order_by('-fecha_pago')
    cantidad_pendientes = pagos.filter(verificado=False).count()

    # 3. Cálculo de Saldo (Solo los VERIFICADOS restan de la deuda)
    pagos_verificados = pagos.filter(verificado=True).aggregate(Sum('monto_usd'))['monto_usd__sum'] or 0
    saldo_restante_usd = float(perfil.canon_mensual) - float(pagos_verificados)
    saldo_restante_bs = saldo_restante_usd * tasa_valor

    # --- PASO 4: PROCESAR EL FORMULARIO ---
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.inquilino = request.user
            monto = float(pago.monto_reportado)

            if pago.moneda == 'BS':
                pago.monto_divisa = monto
                pago.monto_usd = monto / tasa_valor
            else:
                pago.monto_usd = monto
                pago.monto_divisa = monto * tasa_valor
            
            pago.save()
            return redirect('dashboard')
    else:
        form = PagoForm()

    # --- PASO 5: RENDERIZAR TODO AL HTML ---
    return render(request, 'cobranza/dashboard.html', {
        'perfil': perfil,
        'pagos': pagos,
        'form': form,
        'tasa': tasa_valor,
        'saldo_restante_usd': max(0, saldo_restante_usd),
        'saldo_restante_bs': max(0, saldo_restante_bs),
        'cantidad_pendientes': cantidad_pendientes
    })

# No olvides mantener la función de eliminar abajo
@login_required
def eliminar_pago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id, inquilino=request.user)
    if not pago.verificado:
        pago.delete()
    return redirect('dashboard')
