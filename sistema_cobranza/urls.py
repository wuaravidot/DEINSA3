"""
URL configuration for sistema_cobranza project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# Importamos ambas funciones de tu app cobranza
from cobranza.views import dashboard_inquilino, eliminar_pago 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', dashboard_inquilino, name='dashboard'),
    
    # NUEVA RUTA: Para que el botón de borrar de la tabla funcione
    path('pago/eliminar/<int:pago_id>/', eliminar_pago, name='eliminar_pago'),
    
    path('accounts/', include('django.contrib.auth.urls')),
]
