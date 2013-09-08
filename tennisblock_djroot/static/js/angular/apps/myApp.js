'use strict';


// Declare app level module which depends on filters, and services
angular.module('myApp', ['myApp.filters', 'myApp.services', 'myApp.directives']).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/view1', {templateUrl: AngularPartialsBase + '/partial1.html', controller: MyCtrl1});
    $routeProvider.when('/view2', {templateUrl: AngularPartialsBase + '/partial2.html', controller: MyCtrl2});
    $routeProvider.when('/:gardenerid"', {templateUrl: AngularPartialsBase + '/partial1.html', controller: MyCtrl2});
    $routeProvider.otherwise({redirectTo: '/view1'});
  }]);
