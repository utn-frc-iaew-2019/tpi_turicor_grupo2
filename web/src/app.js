var app = angular.module("turicor", ['ngResource']);

app.controller("reservasCtrl", function ($scope, $resource) {
    $scope.title = "Reservas";

    $scope.reserva = {
        pais: null,
        ciudad: null,
    };

    let paises = $resource("/api/paises");
    $scope.paises = paises.query();

    let ciudades = $resource("/api/paises/:paisId/ciudades");
    $scope.ciudades = [];

    $scope.updateCiudades = function () {
        let pais = $scope.reserva.pais;
        $scope.ciudades = ciudades.query({paisId: pais.id});
        $scope.reserva.ciudad = null;
    }

});