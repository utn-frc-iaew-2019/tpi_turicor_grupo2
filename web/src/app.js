var app = angular.module("turicor", ['ngResource']);

app.controller("reservasCtrl", function ($scope, $resource) {
    $scope.title = "Consulta de Vehículos Disponibles";

    $scope.reserva = {
        vendedor: null,
        pais: null,
        ciudad: null,
        desde: null,
        hasta: null,
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

    let vehiculos = $resource("/api/vehiculos");
    $scope.vehiculos = null;
    $scope.buscarVehiculos = function () {
        let reserva = $scope.reserva;
        let params = {
            ciudad_id: reserva.ciudad.id,
            desde: reserva.desde || "2019-01-01T00:00:00", // TODO: Remove default
            hasta: reserva.hasta || "2019-01-05T00:00:00", // TODO: Remove default
        };
        vehiculos.query(params, function (vehiculos) {
            $scope.vehiculos = vehiculos;
        });
    };

});