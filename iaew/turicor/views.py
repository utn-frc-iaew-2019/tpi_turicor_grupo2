from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from zeep import Client


@api_view(['GET'])
def get_paises_list(request, format="application/json"):
    wsdl_settings = settings.IAEW_SETTINGS['wsdl']
    # Get all countries
    client = Client(wsdl=wsdl_settings['url'])
    # cred = client.get_type('ns3:Credentials')

    respuesta = client.service.ConsultarPaises(_soapheaders={'Credentials': wsdl_settings['Credentials']})

    # Serialize
    paises = []
    for pais in respuesta.Paises.PaisEntity:
        paises.append({
            "id": pais.Id,
            "nombre": pais.Nombre
        })

    return Response(paises)
