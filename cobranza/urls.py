from django.urls import path
from . import views

urlpatterns = [
    # Al dejarlo vacío '', la URL será http://127.0.0.1:8000/dashboard/
    path('dashboard/', views.dashboard_inquilino, name='dashboard'),
    path('eliminar_pago/<int:pago_id>/', views.eliminar_pago, name='eliminar_pago'),
]