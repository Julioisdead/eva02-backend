from django.db import models
from django.utils import timezone


class Reserva(models.Model):
    ESTADO_CHOICES = [("Aceptado", "Aceptado"), ("Rechazado", "Rechazado")]

    nombre = models.CharField(max_length=100)
    hora_solicitada = models.IntegerField()
    cupos_disponibles = models.IntegerField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    motivo = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Borrado logico: no se pierde nada, solo se oculta
    eliminado = models.BooleanField(default=False)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"{self.nombre} - {self.hora_solicitada}:00 - {self.estado}"

    def soft_delete(self):
        self.eliminado = True
        self.fecha_eliminacion = timezone.now()
        self.save()  # sin esto no guarda nada
