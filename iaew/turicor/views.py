from django.conf import settings
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
    # Get all countries
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
