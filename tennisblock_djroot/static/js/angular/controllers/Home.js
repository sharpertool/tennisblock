/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 6/14/13
 * Time: 6:51 PM
 */

app.controller('Home', function($scope, $http) {
    $scope.current = {
        name: "Loading..." ,
        gardeners: []
    }
    //$http.get('/api/players/').success(function(data) {
    //#    $scope.gardeners = data;
    //#})
});

