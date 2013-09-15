/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 6/14/13
 * Time: 6:51 PM
 */

app.controller('BlockPlayers', function($scope,$http) {
    $scope.players = [];

    $http.get('/api/blockplayers').success(function(data) {
        $scope.players = data;
    });

});


