"""iaew URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from turicor import views

router = routers.DefaultRouter()

schema_view = get_swagger_view(title='IAEW 2019')

urlpatterns = [
    path('', views.login),
    path('admin/', admin.site.urls),
    path('api/vendedores/', views.vendedores),
    path('api/paises/<int:pais_id>/ciudades/', views.get_ciudades_list),
    path('api/paises/', views.get_paises_list),
    path('api/vehiculos/', views.get_vehiculos_list),
    path('api/vehiculos/<int:vehiculo_id>/reservar', views.reservar_vehiculo),
    path('api/reservas/', views.get_reservas_list),
    path('api/reservas/<codigo>', views.detalle_reserva),
    path('api/reservas/<codigo>/cancelar', views.cancelar_reserva),
    path('api-swagger/', schema_view),

    # Login using api/auth/login/google-oauth2?next={Redirect_URL}
    path('api/auth/', include('social_django.urls', namespace='social')),
]
