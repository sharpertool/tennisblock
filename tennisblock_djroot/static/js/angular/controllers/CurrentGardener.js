'use strict';


    // Declare app level module which depends on filters, and services
//var app = angular.module('featuredgardeners', [])
app.config(['$routeProvider','$locationProvider', function($routeProvider,$locationProvider) {
    $routeProvider
        .when('/', {
            templateUrl: AngularPartialsBase + '/currentGardener.html',
            controller: 'CurrentGardener',
            resolve: {
                // I will cause a 1 second delay
                delay: function($q, $timeout) {
                    var delay = $q.defer();
                    $timeout(delay.resolve, 1000);
                    return delay.promise;
                }
            }
        })
        .when('/:gardenerID', {
            templateUrl: AngularPartialsBase + '/currentGardener.html',
            controller: 'CurrentGardener',
            resolve: {
                // I will cause a 1 second delay
                delay: function($q, $timeout) {
                    var delay = $q.defer();
                    $timeout(delay.resolve, 1000);
                    return delay.promise;
                }
            }
        })
        .otherwise({redirectTo: '/'});

    // This is hella cool, but doesn't work quite right
    //$locationProvider.html5Mode(true);
    //$locationProvider.html5Mode(true).hashPrefix('!');
}]);

app.controller('CurrentGardener', function($scope, $location, $route, $routeParams,$http) {
    $scope.current = {
        name: "Loading..." ,
        current: null,
        mainvideo: null
    };
    $scope.$routeParams = $routeParams;
    $scope.$route = $route;
    $scope.$location = $location;

    //$scope.$on('$viewContentLoaded', function() { initJw()});

    if ($routeParams.gardenerID) {
        console.log("Route with Gardener id:" + $routeParams.gardenerID);
        $http.get('/dapi/gardeners/' + $routeParams.gardenerID).success(function(data) {
            console.log("Loaded featured gardener data: " + $routeParams.gardenerID);
            $scope.current = data;
        })
    } else {
        console.log("Current Gardener route");
        $http.get('/dapi/gardeners/current').success(function(data) {
            console.log("Loaded current gardener data.:");
            $scope.current = data;
        })
    }
});

