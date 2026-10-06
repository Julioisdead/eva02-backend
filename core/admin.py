from django.contrib import admin
from .models import Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "hora_solicitada", "cupos_disponibles",
                    "estado", "motivo", "fecha_creacion")
    list_filter = ("estado", "eliminado")
    search_fields = ("nombre",)
    readonly_fields = ("fecha_eliminacion",)
