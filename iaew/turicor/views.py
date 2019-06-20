from decimal import Decimal

from django.conf import settings
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from zeep import Client


@api_view(['GET'])
def get_paises_list(request):
    wsdl_settings = settings.IAEW_SETTINGS['wsdl']
    # Get all countries
    client = Client(wsdl=wsdl_settings['url'])

    respuesta = client.service.ConsultarPaises(_soapheaders={'Credentials': wsdl_settings['Credentials']})

    # Serialize
    paises = []
    for pais in respuesta.Paises.PaisEntity:
        paises.append({
            "id": pais.Id,
            "nombre": pais.Nombre
        })

    return Response(paises)


@api_view(['GET'])
def get_ciudades_list(request, pais_id):
    wsdl_settings = settings.IAEW_SETTINGS['wsdl']
    # Get ciudades from SOAP
    client = Client(wsdl=wsdl_settings['url'])
    respuesta = client.service.ConsultarCiudades(ConsultarCiudadesRequest={'IdPais': pais_id},
                                                 _soapheaders={'Credentials': wsdl_settings['Credentials']})

    # Serialize
    ciudades = []
    for ciudad in respuesta.Ciudades.CiudadEntity:
        ciudades.append({
            "id": ciudad.Id,
            "nombre": ciudad.Nombre
        })

    return Response(ciudades)


@api_view(['GET'])
def get_vehiculos_list(request):
    # Get params
    ciudad_id = request.GET.get('ciudad_id', None)
    try:
        desde = parse_datetime(request.GET.get('desde', None))  # yyyy-mm-ddThh:mm:ss (optional timezone:-0300)
        hasta = parse_datetime(request.GET.get('hasta', None))  # yyyy-mm-ddThh:mm:ss
    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)  # Valid format but non-existent datetime.

    if ciudad_id is None or not ciudad_id.isdigit() or desde is None or hasta is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    wsdl_settings = settings.IAEW_SETTINGS['wsdl']
    # Get vehiculos from SOAP
    client = Client(wsdl=wsdl_settings['url'])

    request = {
        'IdCiudad': ciudad_id,
        'FechaHoraRetiro': desde,
        'FechaHoraDevolucion': hasta
    }
    respuesta = client.service.ConsultarVehiculosDisponibles(
        ConsultarVehiculosRequest=request,
        _soapheaders={'Credentials': wsdl_settings['Credentials']})

    # Serialize
    vehiculos = []
    for vehiculo in respuesta.VehiculosEncontrados.VehiculoModel:
        vehiculos.append({
            "id": vehiculo.Id,
            "vehiculo_ciudad_id": vehiculo.VehiculoCiudadId,
            "ciudad_id": vehiculo.CiudadId,
            "marca": vehiculo.Marca,
            "modelo": vehiculo.Modelo,
            "cantidad_disponible": vehiculo.CantidadDisponible,
            "precio_alquiler": vehiculo.PrecioPorDia / Decimal(1 - settings.IAEW_SETTINGS['ganancia']),
            "descripcion": {
                "puntaje": vehiculo.Puntaje,
                "cantidad_puertas": vehiculo.CantidadPuertas,
                "aire_acondicionado": vehiculo.TieneAireAcon,
                "direccion_asistida": vehiculo.TieneDireccion,
                "tipo_cambio": vehiculo.TipoCambio
            }
        })

    return Response(vehiculos)
