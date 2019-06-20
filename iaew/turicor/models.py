# Create your models here.
from django.db import models


class Reserva(models.Model):
    LUGAR_CHOICES = (
        ('Aeropuerto', 'Aeropuerto'),
        ('TerminalBuses', 'Terminal de Colectivos'),
        ('Hotel', 'Hotel')
    )

    codigo = models.CharField(unique=True, max_length=12)
    estado = models.CharField(max_length=64)
    fecha_reserva = models.DateTimeField()
    fecha_cancelacion = models.DateTimeField(blank=True, null=True)
    fecha_hora_retiro = models.DateTimeField()
    fecha_hora_devolucion = models.DateTimeField()
    lugar_retiro = models.CharField(choices=LUGAR_CHOICES, max_length=13)
    lugar_devolucion = models.CharField(choices=LUGAR_CHOICES, max_length=13)
    cliente = models.ForeignKey(to="Cliente", on_delete=models.PROTECT)
    precio_costo = models.IntegerField()
    precio_venta = models.IntegerField()
    vehiculo_id = models.IntegerField()


class Cliente(models.Model):
    nombre = models.CharField(max_length=64)
    apellido = models.CharField(max_length=64)
    dni = models.PositiveIntegerField()

