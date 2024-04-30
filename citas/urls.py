from django.urls import path

from .views import reservar_cita, filtrar_disponibilidad, confirmacion_pago, ProcesoPago

citas_patterns = ([
  path('', reservar_cita, name='cita-form'),
  path('disponibilidad/', filtrar_disponibilidad, name='disponibilidad'),
  path('procesar-pago/<str:cita_id>/', ProcesoPago.as_view(), name='proceso_pago'),
  path('confirmacion-pago/<str:cita_id>/', confirmacion_pago, name='confirmacion_pago'),

], 'citas')