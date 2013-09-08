/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 6/15/13
 * Time: 7:55 PM
 */

app.directive('jwvideo',function() {
    var linkFn;
    linkFn = function($scope,element,attrs) {

        var dataChanged = function() {
            if ($scope.current.mainvideo === null) {
                return;
            }


            var sources = [];
            _.each($scope.current.mainvideo.paths,function(path) {
                if (path.host === 's3') {
                    //sources.push({
                    //    file: path.path,
                    //    label: path.quality
                    //})
                } else if (path.host === 'vimeo') {
                    if (path.format === 'mp4') {
                        sources.push({
                            file: path.path,
                            label: path.quality
                        })
                    }
                }
            });

            if (sources.length === 0) {
                sources = [
                    //{
                    //    file: this.url
                    //},
                    //{file: '/media/FeaturedGardener/JulianneHaller.mp4', label: 'HD' },
                    //{file: '/media/FeaturedGardener/JulianneHaller_sd.mp4', label: 'SD' },
                    {file: 'https://s3-us-west-2.amazonaws.com/featured-gardener/JulianneHaller.mp4', label: 'HD'},
                    {file: 'https://s3-us-west-2.amazonaws.com/featured-gardener/JulianneHaller_sd.mp4', label: 'SD'}
                ];

            }

            var id = element.attr('id');
            $scope.player = new GBJWPlayer(id,sources, {'image':null,'tracks' : []});
            $scope.player.init();
            var video = $scope.player.video;

            var onTimeUpdate = function() {
                var pos = video.getCurrentTime();

                $('#videopos').val(pos);
                $('#videopos').text(pos);
            };

            $('#jumppoints').on('click','li',function() {
                var seekPos = $(this).attr('seek');
                $scope.player.seek(seekPos);
            });

        }

        $scope.$watch('current', function(newValue, oldValue) {
            if (newValue) {
                console.log("I see a data change!");
                dataChanged();
            }
        }, true);

    };

    return {
        restrict: 'E',
        link: linkFn,
    };
});


