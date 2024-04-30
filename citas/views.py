from django.shortcuts import render, redirect,  get_object_or_404
from datetime import datetime
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.views import View
from django.urls import reverse
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
      return redirect(reverse('citas:proceso_pago', args=[cita.cita_id]))  # Redirigir a una página de confirmación
    except ValidationError as e:
        return HttpResponse(f"Error en la validación de los datos: {e.messages}", status=400)

  else:
			# Mostrar el formulario de reserva de cita
			return render(request, 'citas/reservar_cita.html')

def filtrar_disponibilidad(request):
    # Get the selected date from the request
    selected_date = request.GET.get('fecha')

    # Convert the selected date string to a datetime object
    if selected_date is not None:
      try:
        selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
      except:
        return JsonResponse({'error': 'Fecha inválida'}, status=400)
    else:
      return JsonResponse({'error': 'Formulario inválido'}, status=400)
      			
    # Filter available time slots for the selected date
    available_slots = []
    for hour_slot in HORAS_DISPONIBLES:
        # Check if there are any appointments scheduled for the selected date and time slot
        appointments = Cita.objects.filter(fecha=selected_date_obj, hora=hour_slot[0])
        if not appointments.exists():
            available_slots.append(hour_slot)

      # Prepare JSON response
    response_data = {
        'fecha_seleccionada': selected_date_obj.strftime('%Y-%m-%d'),
        'horas_disponibles': [{'hora:': slot[0]} for slot in available_slots],
    }

    return JsonResponse(response_data)

# Procesar el pago

class ProcesoPago(View):
    template_name = 'citas/procesar_pago.html'
    precio = int(50 * 100) # Centavos de euro para un cargo de 10 euros

    def get(self, request, *args, **kwargs):
        cita_id = self.kwargs.get('cita_id')
        cita = get_object_or_404(Cita, cita_id=cita_id)


        if cita.estado == 'confirmada':
            return redirect('citas:cita-form')

        context = {
          'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
          'cita': cita,
          'precio': self.precio
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        token = request.POST.get('stripeToken')
        cita_id = self.kwargs.get('cita_id')
        cita = get_object_or_404(Cita, cita_id=cita_id)
        print(cita_id)
        print(cita)

        try:
            # Crea el cargo en Stripe
            charge = stripe.Charge.create(
                amount=self.precio,  
                currency='eur',
                description='Pago por cita',
                source=token,
                receipt_email=cita.email,
                metadata={
                  'user_email': cita.email,  
                  'cita_id': 'cita456'         
                },
            )

            # Actualizar el estado de la cita a 'confirmada'
            cita.estado = 'confirmada'
            cita.save()

            return redirect(reverse('citas:confirmacion_pago', args=[cita_id]))
        except stripe.error.StripeError as e:
            return render(request, 'citas/error_pago.html', {'error': str(e)})
        
def confirmacion_pago(request, cita_id):
    cita = get_object_or_404(Cita, cita_id=cita_id)
    if cita.estado == 'confirmada':
        mensaje = "Gracias por su pago. Su cita ha sido confirmada."
    else:
        mensaje = "Hubo un error al procesar su cita. Por favor, contacte con soporte."
    
    return render(request, 'citas/confirmacion_pago.html', {
        'cita': cita,
        'mensaje': mensaje
    })