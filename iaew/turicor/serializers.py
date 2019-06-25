from rest_framework import serializers

from .models import Reserva, Vendedor


class ReservasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ('codigo', 'fecha_reserva', 'fecha_cancelacion', 'precio_venta')


class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = ('id', 'nombre')
