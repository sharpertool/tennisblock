/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 6/14/13
 * Time: 6:51 PM
 */

tennisblockapp.controller('LatestBuzz', function($scope,$http,BlockBuzz) {
    BlockBuzz.query(function(data) {
        $scope.buzzitems = data;
    });
});

