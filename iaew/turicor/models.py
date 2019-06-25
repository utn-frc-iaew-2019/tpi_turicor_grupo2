from django.contrib.auth.models import User
from django.db import models


class Reserva(models.Model):
    codigo = models.CharField(unique=True, max_length=12)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    fecha_cancelacion = models.DateTimeField(blank=True, null=True)
    cliente = models.ForeignKey(to="Cliente", on_delete=models.PROTECT)
    vendedor = models.ForeignKey("Vendedor", on_delete=models.SET_NULL, null=True, blank=True)
    precio_costo = models.IntegerField()
    precio_venta = models.IntegerField()


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.PositiveIntegerField()


class Vendedor(models.Model):
    nombre = models.CharField(max_length=64)
