# Sistema de Reserva de Citas con Pago mediante Stripe Checkout

Desarrollado por Daniel Casado, este proyecto ofrece un sistema de reserva de citas que permite a los usuarios seleccionar una fecha y hora, proporcionar detalles personales y efectuar el pago de la cita utilizando Stripe Checkout.

## Características

- **Reserva de Citas**: Los usuarios pueden elegir entre fechas y horas disponibles para programar una cita.
- **Validación de Disponibilidad**: El sistema verifica la disponibilidad en tiempo real para prevenir reservas dobles.
- **Integración con Stripe Checkout**: Implementa una pasarela de pago segura con Stripe para procesar pagos.

## Tecnologías Utilizadas
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS y Javascript
- **Pagos**: Stripe Checkout

## Instrucciones:
Instalaremos las dependencias.
```bash
pip install -r requirements.txt
```

#### Stripe, Striple CLI y Webhooks:

Vamos a necesitar también instalar StripeCLI, para poder hacer uso de los webhooks en local.

Visita [GitHub](https://github.com/stripe/stripe-cli/releases/tag/v1.19.4) para descargarlo.

Antes de configurar esta parte tendrémos que crear un webhook sencillo, que este escuchando el evento: `checkout.session.completed`.
- Dirigete a tu dashboard de Stripe y a la seccion de Desarrolladores.
- Añade un punto de conexión y selecciona el evento `checkout.session.completed` de la lista.
- Una vez agregado el endpoint, Stripe te proporcionará un "Signing secret". 
- Tendrás que configurar esta clave en `citas/views.py` en la vista `stripe_webhook`.

Vamos con la parte de stripe CLI:

Una vez instalado inicia sesión mediante este comando:
```bash
stripe login
```

Para escuchar eventos de `checkout.session.completed` localmente, ejecuta:
```bash
stripe listen --forward-to https://localhost:8000/webhooks/stripe
```