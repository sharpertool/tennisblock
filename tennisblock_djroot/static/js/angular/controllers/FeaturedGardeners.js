/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 6/14/13
 * Time: 6:51 PM
 */

app.controller('FeaturedGardeners', function($scope, $http) {
    $scope.current = {
        name: "Loading..." ,
        gardeners: []
    }
    $http.get('/dapi/gardeners/').success(function(data) {
        $scope.gardeners = data;
    })
});

