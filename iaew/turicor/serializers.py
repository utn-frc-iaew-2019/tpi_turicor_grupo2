from rest_framework import serializers

from turicor.models import Reserva


class ReservasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ('codigo', 'fecha_reserva', 'fecha_cancelacion', 'precio_venta')
