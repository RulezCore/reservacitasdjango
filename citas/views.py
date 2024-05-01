from django.shortcuts import render, redirect,  get_object_or_404
from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.views import View
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings

from .models import Cita, HORAS_DISPONIBLES

stripe.api_key = settings.STRIPE_SECRET_KEY


def reservar_cita(request):
    if request.method == 'POST':
      nombre_completo = request.POST.get('nombre_completo')
      telefono_contacto = request.POST.get('telefono_contacto')
      email = request.POST.get('email')
      describe_tu_caso = request.POST.get('describe_tu_caso')
      fecha = request.POST.get('fecha')
      hora = request.POST.get('hora')

      # Intentar guardar el formulario en el modelo
      try:
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()

        cita = Cita(
            nombre_completo=nombre_completo,
            telefono_contacto=telefono_contacto,
            email=email,
            describe_tu_caso=describe_tu_caso,
            fecha=fecha_obj,
            hora=hora,
            estado='pendiente'
        )
        cita.full_clean()
        cita.save()
        # Redirigir a una página de confirmación
        return redirect(reverse('citas:proceso_pago', args=[cita.cita_id]))
      except ValidationError as e:
        return HttpResponse(f"Error en la validación de los datos: {e.messages}", status=400)

    else:
        # Mostrar el formulario de reserva de cita
        return render(request, 'citas/reservar_cita.html')


def filtrar_disponibilidad(request):
    selected_date = request.GET.get('fecha')
    if not selected_date:
        return JsonResponse({'error': 'Formulario inválido'}, status=400)

    try:
        selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
    except ValueError:
        return JsonResponse({'error': 'Fecha inválida'}, status=400)

    now = datetime.now()
    available_slots = []
    buffer_time = timedelta(minutes=15)  # Establecemos un buffer de 15 minutos

    is_today = selected_date_obj.date() == now.date()

    for hour_slot in HORAS_DISPONIBLES:
        slot_time = datetime.strptime(hour_slot[0], "%H:%M").time()
        # Calcular el tiempo actual más el buffer
        current_plus_buffer = (datetime.combine(datetime.today(), now.time()) + buffer_time).time()

        # Si la fecha seleccionada es hoy y la hora del slot es menor o igual al tiempo actual más el buffer, continuar
        if is_today and slot_time <= current_plus_buffer:
            continue  # Salta este slot porque está en el pasado o demasiado cerca en el futuro

        # Verificar si hay citas programadas para la fecha y hora seleccionada
        if not Cita.objects.filter(fecha=selected_date_obj, hora=hour_slot[0]).exists():
            available_slots.append(hour_slot)

    response_data = {
        'fecha_seleccionada': selected_date_obj.strftime('%Y-%m-%d'),
        'horas_disponibles': [{'hora': slot[0]} for slot in available_slots],
    }

    return JsonResponse(response_data)

# Procesar el pago, manejar WebHooks


class ProcesoPago(View):
    def get(self, request, *args, **kwargs):
        cita_id = self.kwargs.get('cita_id')
        cita = get_object_or_404(Cita, cita_id=cita_id)
        price = int(50*100)

        if cita.estado == 'confirmada':
            return redirect('citas:cita-form')

        # Crear la sesión de Checkout de Stripe
        try:
          checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card', "paypal"],
            customer_email=cita.email,
            line_items=[{
              'price_data': {
                'currency': 'eur',
                'unit_amount': price,
                # 'email': cita.email,
                'product_data': {
                    'name': f'Pago por cita de {cita.nombre_completo}',
                    'description': f'Cita para el dia {cita.fecha} a las {cita.hora}',
                },
              },

              'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('citas:confirmacion_pago', args=[cita_id])) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse('citas:confirmacion_pago', args=[cita_id])) + '?session_id={CHECKOUT_SESSION_ID}',
            metadata={
                'cita_id': str(cita_id)
            }
          )
        except Exception as e:
            return render(request, 'citas/error_pago.html', {'error': str(e)})

        return HttpResponseRedirect(checkout_session.url)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = ''

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Cuerpo de la solicitud inválido
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Firma de webhook inválida
        return HttpResponse(status=400)

    # Procesa el evento
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_session(session)

    return HttpResponse(status=200)


def handle_checkout_session(session):
    # Suponiendo que pasas un identificador personalizado en 'metadata' al crear la sesión
    cita_id = session['metadata']['cita_id']
    try:
        cita = Cita.objects.get(cita_id=cita_id)
        if cita.estado != 'confirmada':
            cita.estado = 'confirmada'
            cita.save()
            # Aquí podrías añadir lógica para enviar un correo de confirmación, etc.
        return JsonResponse({'status': 'success'}, status=200)
    except Cita.DoesNotExist:
        return JsonResponse({'error': 'Cita no encontrada'}, status=404)


def confirmacion_pago(request, cita_id):
  cita = get_object_or_404(Cita, cita_id=cita_id)
  session_id = request.GET.get('session_id')
  if session_id:
      session = stripe.checkout.Session.retrieve(session_id)

      if session.payment_status == 'paid':
          return render(request, 'citas/confirmacion_pago.html', {'cita': cita, })
      else:
          cita.delete()
          return redirect(reverse('citas:cita-form') + '?error=pago_cancelado')
  return redirect(reverse('citas:cita-form'))