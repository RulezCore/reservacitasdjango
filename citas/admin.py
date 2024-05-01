from django.contrib import admin
from django.utils.html import format_html
from .models import Cita

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('cita_id', 'fecha', 'hora', 'nombre_completo', 'email', 'show_estado')
    list_filter = ('estado', 'fecha', 'nombre_completo', 'telefono_contacto', 'email', )
    search_fields = ('cita_id', 'nombre_completo', 'email', 'telefono_contacto')
    ordering = ('-fecha', '-hora')

    def show_estado(self, obj):
        if obj.estado == 'confirmada':
            return format_html('<span style="color: green;">&#10003;</span>')
        elif obj.estado == 'pendiente':
            return format_html('<span style="color: orange;">&#8226;&#8226;&#8226;</span>')
        elif obj.estado == 'cancelada':
            return format_html('<span style="color: red;">&#10007;</span>')
    show_estado.short_description = 'Estado'
