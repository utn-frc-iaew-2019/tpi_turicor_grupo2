from decimal import Decimal

from django.conf import settings
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from zeep import Client

from turicor.models import Reserva, Cliente
from turicor.serializers import ReservasSerializer


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
            # "id": vehiculo.Id,
            "id": vehiculo.VehiculoCiudadId,
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


@api_view(['POST'])
def reservar_vehiculo(request, vehiculo_id):
    lugar_retiro = request.data.get('lugar_retiro', None)
    lugar_devolucion = request.data.get('lugar_devolucion', None)
    if None in [lugar_retiro, lugar_devolucion]:
        return Response("Lugar invalido", status=status.HTTP_400_BAD_REQUEST)

    try:
        desde = parse_datetime(request.data.get('desde', None))  # yyyy-mm-ddThh:mm:ss (optional timezone:-0300)
        hasta = parse_datetime(request.data.get('hasta', None))  # yyyy-mm-ddThh:mm:ss
    except ValueError or TypeError:
        return Response("Fechas invalidas",
                        status=status.HTTP_400_BAD_REQUEST)  # Valid format but non-existent datetime.

    # Make reserva on SOAP
    wsdl_settings = settings.IAEW_SETTINGS['wsdl']
    client = Client(wsdl=wsdl_settings['url'])

    factory = client.type_factory('ns2')

    request = factory.ReservarVehiculoRequest(
        IdVehiculoCiudad=vehiculo_id,
        ApellidoNombreCliente="Prueba",  # TODO: Get client info from auth.
        NroDocumentoCliente=11111111,
        FechaHoraRetiro=desde,
        FechaHoraDevolucion=hasta,
        LugarRetiro=factory.LugarRetiroDevolucion(lugar_retiro),  # TODO: Validar 'Aeropuerto', 'TerminalBuses', 'Hotel'
        LugarDevolucion=factory.LugarRetiroDevolucion(lugar_devolucion)
    )

    respuesta = client.service.ReservarVehiculo(
        ReservarVehiculoRequest=request,
        _soapheaders={'Credentials': wsdl_settings['Credentials']})

    # TODO: Remove this. Use Auth.
    # DEBUG ONLY
    Cliente.objects.get_or_create(pk=1, nombre="Prueba", apellido="Prueba", dni=1111111)

    # Serialize
    # respuesta.Reserva
    reserva = Reserva(
        codigo=respuesta.Reserva.CodigoReserva,
        cliente_id=1,
        precio_costo=respuesta.Reserva.TotalReserva,
        precio_venta=respuesta.Reserva.TotalReserva / Decimal(1 - settings.IAEW_SETTINGS['ganancia'])
    )
    reserva.save()

    return Response({
        "codigo_reserva": reserva.codigo
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_reservas_list(request):
    cliente_id = 1  # TODO: Get client id.

    reservas = ReservasSerializer(Reserva.objects.filter(cliente_id=cliente_id), many=True)

    return Response(reservas.data)


@api_view(['GET'])
def detalle_reserva(request, codigo):
    wsdl_settings = settings.IAEW_SETTINGS['wsdl']
    # Get ciudades from SOAP
    client = Client(wsdl=wsdl_settings['url'])
    respuesta = client.service.ConsultarReserva(
        ConsultarReservaRequest={'CodigoReserva': codigo},
        _soapheaders={'Credentials': wsdl_settings['Credentials']})

    # Get precio reserva from BD
    precio = Reserva.objects.get(codigo=codigo).precio_venta

    # Serialize
    reserva = {
        "codigo": respuesta.Reserva.CodigoReserva,
        "nombre_apellido": respuesta.Reserva.ApellidoNombreCliente,
        "dni": respuesta.Reserva.NroDocumentoCliente,
        "estado": respuesta.Reserva.Estado,
        "fecha_reserva": respuesta.Reserva.FechaReserva,
        "fecha_cancelacion": respuesta.Reserva.FechaCancelacion,
        "fecha_hora_retiro": respuesta.Reserva.FechaHoraRetiro,
        "fecha_hora_devolucion": respuesta.Reserva.FechaHoraDevolucion,
        "lugar_retiro": respuesta.Reserva.LugarRetiro,
        "lugar_devolucion": respuesta.Reserva.LugarDevolucion,
        "precio": precio,
        "vehiculo_id": respuesta.Reserva.VehiculoPorCiudadId,
        # respuesta.Reserva.VehiculoPorCiudadEntity.VehiculoEntity vuelve vacio.
        # No estan los datos del vehiculo ni la ciudad.
    }

    return Response(reserva)


@api_view(['POST'])
def cancelar_reserva(request, codigo):
    wsdl_settings = settings.IAEW_SETTINGS['wsdl']
    client = Client(wsdl=wsdl_settings['url'])
    respuesta = client.service.CancelarReserva(
        CancelarReservaRequest={'CodigoReserva': codigo},
        _soapheaders={'Credentials': wsdl_settings['Credentials']})

    Reserva.objects.filter(codigo=codigo).update(fecha_cancelacion=respuesta.TimeStamp)

    return Response("Reserva cancelada.")
