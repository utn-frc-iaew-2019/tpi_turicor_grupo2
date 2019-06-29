var app = angular.module("turicor", ['ngResource']);

app.controller("reservasCtrl", function ($scope, $resource) {
    $scope.title = "Consulta de Vehículos Disponibles";

    $scope.LUGAR_OPTIONS = [
        "Aeropuerto",
        "TerminalBuses",
        "Hotel"
    ];

    $scope.reserva = {
        vendedor: null,
        pais: null,
        ciudad: null,
        desde: "2019-01-01T00:00:0",
        hasta: "2019-01-03T00:00:0",
        lugar_retiro: $scope.LUGAR_OPTIONS[0],
        lugar_devolucion: $scope.LUGAR_OPTIONS[0],
    };

    $scope.vendedores = $resource("/api/vendedores").query();

    let paises = $resource("/api/paises");
    paises.query({}, function (paises) {
        $scope.paises = paises;
        $scope.reserva.pais = paises[0];
        $scope.updateCiudades();
    });

    let ciudades = $resource("/api/paises/:paisId/ciudades");
    $scope.ciudades = [];

    $scope.updateCiudades = function () {
        let pais = $scope.reserva.pais;
        ciudades.query({paisId: pais.id}, function (ciudades) {
            $scope.ciudades = ciudades;
            $scope.reserva.ciudad = ciudades[0];
        });
    };

    let vehiculos = $resource("/api/vehiculos", {}, {
        reservar: {
            method: "POST",
            url: "/api/vehiculos/:vehiculoId/reservar",
        }
    });
    $scope.vehiculos = null;
    $scope.buscarVehiculos = function () {
        let reserva = $scope.reserva;
        let params = {
            ciudad_id: reserva.ciudad.id,
            desde: reserva.desde,
            hasta: reserva.hasta,
        };
        vehiculos.query(params, function (vehiculos) {
            $scope.vehiculos = vehiculos;
        });
    };


    $scope.reservar = function (reserva, vehiculo) {
        let body = {
            desde: reserva.desde,
            hasta: reserva.hasta,
            lugar_retiro: reserva.lugar_retiro,
            lugar_devolucion: reserva.lugar_devolucion
        };
        body.vehiculoId = vehiculo.id;
        vehiculos.reservar({vehiculoId: vehiculo.id}, body, function () {
            $scope.vehiculos = null;
        });
    };

});