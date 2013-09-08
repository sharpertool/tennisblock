'use strict';

/*
app.config(['$routeProvider', function($routeProvider) {
    $routeProvider.
        when('/nurseries', {templateUrl: 'partials/partial1.html',   controller: NurseryListCtrl}).
        when('/nurseries/:nurseryId', {templateUrl: 'partials/partial2.html', controller: NurseryDetailCtrl}).
        otherwise({redirectTo: '/'});
*/

app.controller('NurseryListCtrl', ['$scope','$http','$routeParams','$route','$location',function($http,$scope,$routeParams,$route,$location) {
    $scope.loading = true;
    $scope.$routeParams = $routeParams;
    $scope.$route = $route;
    $scope.$location = $location;

    $scope.thumbphoto = function(photos) {
        return _.find(photos.files,function(file) { return file.width < 300; });
    };

    $scope.fullphoto = function(photos) {
        return _.find(photos.files,function(file) { return file.width > 300; });
    };

    $scope.phototitle = function(photos) {
        var full = this.fullphoto(photos);
        return full.title;
    };

    $scope.hasPhotos = function(nursery) {
        return nursery.photos.length > 0;
    };

    $scope.nextGallery = function() {
        var id = $scope.galleryId;
        $scope.galleryId += 1;
        return 'gallery' + id;
    };

    $scope.nextThumbId= function() {
        var id = $scope.thumbId;
        $scope.thumbId += 1;
        return 'thumb' + id;
    };

    $http.get('/dapi/nurseries').success(function(data) {
        console.log("Loaded Nureries");
        $scope.nurseries = data;
        _.each($scope.nurseries,function(nursery) {
            if (nursery.photos.length > 0) {
                nursery.hasPhotos = 1;

                nursery.firstPhoto = nursery.photos.pop();
                nursery.firstThumb = _.find(nursery.firstPhoto.files,function(file) { return file.width < 300; });
                nursery.firstFull  = _.find(nursery.firstPhoto.files,function(file) { return file.width > 300; });
                nursery.firstTitle = nursery.firstPhoto.title;

                _.each(nursery.photos,function(photo) {
                    photo.thumb = _.find(photo.files,function(file) { return file.width < 300; });
                    photo.full = _.find(photo.files,function(file) { return file.width > 300; });
                });
            } else {
                nursery.hasPhotos = 0;
            }

        });
        $scope.loading = false;
        $scope.galleryId = 0;
        $scope.thumbId = 0;
        $scope.firstPhoto = null;
    });

}]);


