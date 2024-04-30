from django.db import models
from django.core.validators import ValidationError
from shortuuidfield import ShortUUIDField
import shortuuid

CITA_STATES = (
  ('pendiente', 'Pendiente'),
  ('confirmada', 'Confirmada'),
  ('cancelada', 'Cancelada')
)

HORAS_DISPONIBLES = (
    ('09:00', '09:00'),
    ('10:10', '10:10'),
    ('11:20', '11:20'),
    ('12:30', '12:30'),
    ('13:40', '13:40'),
    ('16:00', '16:00'),
    ('17:10', '17:10'),
    ('18:20', '18:20'),
)

# Create your models here.
class Cita(models.Model):
  cita_id = ShortUUIDField(unique=True, editable=False, auto=True)
  nombre_completo = models.CharField(max_length=255)
  telefono_contacto = models.CharField(max_length=20)
  email = models.EmailField()
  describe_tu_caso = models.TextField()
  fecha = models.DateField()
  hora = models.CharField(max_length=25, choices=HORAS_DISPONIBLES)
  estado = models.CharField(max_length=20, choices=CITA_STATES, default='pendiente')
  fecha_creacion = models.DateTimeField(auto_now_add=True)

  
  def clean(self):
    # Comprobar que el campo fecha no es None
    if self.fecha is None:
            raise ValidationError("La fecha no puede estar vacía.")

    # Comprobar si la fecha de la cita es un fin de semana
    if self.fecha.weekday() in (5, 6):  # 5 = Sábado, 6 = Domingo
        raise ValidationError("Las citas no pueden ser programadas en fines de semana.")
    
    # Verificar que la hora esté en la lista de horas disponibles
    if self.hora not in [hora[0] for hora in HORAS_DISPONIBLES]:
        raise ValidationError("La hora seleccionada no está disponible.")

    # Comprobar si ya existe una cita en la misma fecha y hora
    if Cita.objects.filter(fecha=self.fecha, hora=self.hora).exclude(id=self.id).exists():
        raise ValidationError("Ya existe una cita programada para esta fecha y hora.")
      
  def save(self, *args, **kwargs):
    self.full_clean()  # Llama a clean y hace la validación completa
    super().save(*args, **kwargs)

  def __str__(self):
    return f'Dia {self.fecha} - Hora: {self.hora} - Estado: {self.estado}'
