/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 6/14/13
 * Time: 6:51 PM
 */

tennisblockapp.controller('BlockPlayers', function($scope,BlockPlayers) {
    $scope.players = {
        'guys'          : [],
        'gals'          : [],
        'couples'       : [],
        'initialized'   : false
    };

    BlockPlayers.query(function(data) {
        $scope.players.guys = data.guys;
        $scope.players.gals = data.gals;
        $scope.players.couples = _.zip($scope.players.guys,$scope.players.gals);
        $scope.players.initialized = true;
        //updateInitialized();
    });

});


