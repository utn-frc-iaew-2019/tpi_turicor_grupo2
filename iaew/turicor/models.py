# Create your models here.
from django.db import models


class Reserva(models.Model):
    codigo = models.IntegerField(unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(to="Cliente", on_delete=models.PROTECT)
    vendedor = models.ForeignKey(to="Vendedor", on_delete=models.PROTECT)
    precio_costo = models.IntegerField()
    precio_venta = models.IntegerField()
    vehiculo_id = models.IntegerField()
    ciudad_id = models.IntegerField()
    pais_id = models.IntegerField()


class Cliente(models.Model):
    nombre = models.CharField(max_length=64)
    apellido = models.CharField(max_length=64)
    dni = models.PositiveIntegerField()


class Vendedor(models.Model):
    nombre = models.CharField(max_length=64)
