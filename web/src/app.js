var app = angular.module("turicor", ['ngResource']);

app.controller("vehiculosCtrl", function ($scope, $resource) {
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
        desde: "2019-01-01T00:00:00",
        hasta: "2019-01-03T00:00:00",
        lugar_retiro: $scope.LUGAR_OPTIONS[0],
        lugar_devolucion: $scope.LUGAR_OPTIONS[0],
    };

    $scope.vendedores = $resource("/api/vendedores").query(function (vendedores) {
        $scope.reserva.vendedor = vendedores[0];
    });

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
        $scope.reserva.ciudad = null;
        $scope.ciudades = null;
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
            lugar_devolucion: reserva.lugar_devolucion,
            vendedor_id: reserva.vendedor ? reserva.vendedor.id : null
        };
        body.vehiculoId = vehiculo.id;
        vehiculos.reservar({vehiculoId: vehiculo.id}, body, function () {
            $scope.vehiculos = null;
        });
    };

});

app.controller("reservasCtrl", function ($scope, $resource) {
    $scope.title = "Mis Reservas";

    $scope.viewReserva = null


    let reservasAPI = $resource("/api/reservas/:reservaCodigo", {}, {
        all: {
            url: "/api/reservas",
            isArray: true
        },
        cancelar: {
            method: "POST",
            url: "/api/reservas/:reservaCodigo/cancelar"
        }
    });

    $scope.reservas = reservasAPI.all();


    $scope.cancelar = function (reserva) {
        reservasAPI.cancelar({reservaCodigo: reserva.codigo}, {}, function () {
            $scope.reservas = reservasAPI.all();
        })
    };

    $scope.detalle = function (reserva) {
        reservasAPI.get({reservaCodigo: reserva.codigo}, function (detalle) {
            $scope.viewReserva = detalle;
        });

    };

    $scope.lista = function () {
        $scope.viewReserva = null;
    }

});