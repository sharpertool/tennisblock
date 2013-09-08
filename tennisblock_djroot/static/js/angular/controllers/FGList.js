'use strict';

/* Controllers */

function FGList($scope,$http,$routeParams) {
    $scope.thisWeekid = 0;
    $http.get('/data/featuredGardeners.json').success(function(data) {
        $scope.gardeners = data;
        $scope.thisWeek = data[$scope.thisWeekid];
    });
}
FGList.$inject = ['$scope','$http','$routeParams'];


function FeaturedGardener($scope,$http,$routeParams) {
    $http.get('/data/featuredGardeners.json').success(function(data) {
        $scope.gardeners = data;
    });
    $scope.gardenerid = $routeParams.gardenerid;
}
FeaturedGardener.$inject = ['$scope','$http','$routeParams'];

