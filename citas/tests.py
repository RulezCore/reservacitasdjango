from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import Cita
from datetime import date

# TESTS DE MODELO
class CitaModelTest(TestCase):

  def test_crear_cita_fin_de_semana(self):
    """ Verifica que no se pueden crear citas los fines de semana """
    with self.assertRaises(ValidationError):
        cita = Cita(
            nombre_completo="John Doe",
            telefono_contacto="1234567890",
            email="john@example.com",
            describe_tu_caso="Consulta de prueba",
            fecha=datetime(2024, 4, 28).date(),  # Asumiendo que es un domingo
            hora="10:10",
            estado='pendiente'
        )
        cita.full_clean()

  def test_crear_cita_hora_no_disponible(self):
    """ Verifica que no se pueden crear citas en horas no disponibles """
    with self.assertRaises(ValidationError):
        cita = Cita(
            nombre_completo="John Doe",
            telefono_contacto="1234567890",
            email="john@example.com",
            describe_tu_caso="Consulta de prueba",
            fecha=datetime(2024, 4, 25).date(),  # Asumiendo que es un día laboral
            hora="08:00",  # Hora no disponible
            estado='pendiente'
        )
        cita.full_clean()

  def test_crear_cita_duplicada(self):
    """ Verifica que no se pueden crear citas duplicadas """
    Cita.objects.create(
        nombre_completo="John Doe",
        telefono_contacto="1234567890",
        email="john@example.com",
        describe_tu_caso="Consulta inicial",
        fecha=datetime(2024, 4, 25).date(),
        hora="09:00",
        estado='pendiente'
    )
    with self.assertRaises(ValidationError):
        cita = Cita(
            nombre_completo="Jane Doe",
            telefono_contacto="0987654321",
            email="jane@example.com",
            describe_tu_caso="Consulta de seguimiento",
            fecha=datetime(2024, 4, 25).date(),
            hora="09:00",
            estado='pendiente'
        )
        cita.full_clean()
  
  def test_campos_vacios(self):
    """Test para verificar que no se pueden dejar campos requeridos vacíos."""
    try:
        cita = Cita(
            nombre_completo=None,  # Campo vacío
            telefono_contacto='',  # Campo vacío
            email='',  # Campo vacío
            describe_tu_caso='',  # Campo vacío
            fecha=None,  # Campo vacío
            hora=None,  # Campo vacío
            estado='pendiente'  # Este tiene un valor predeterminado y no está vacío
        )
        cita.full_clean()  # Esto debería lanzar ValidationError
    except ValidationError as e:
        self.assertTrue('nombre_completo' in e.message_dict)  # Verifica que el campo esté en el dict de errores
        self.assertTrue('telefono_contacto' in e.message_dict)
        self.assertTrue('email' in e.message_dict)
        self.assertTrue('describe_tu_caso' in e.message_dict)
        self.assertTrue('fecha' in e.message_dict)
        self.assertTrue('hora' in e.message_dict)
    else:
        self.fail("ValidationError no fue lanzada con campos vacíos")


