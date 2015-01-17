/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 10/20/13
 * Time: 2:44 PM
 */

tennisblockapp.directive('scheduleMatches',['TeamSchedule','PickTeams','$q',
    function(TeamSchedule,PickTeams,$q) {
        // Initialization

        return {
            priority: 10,
            restrict: 'EA',
            //require: '^blockMembers',
            controller: 'BlockSchedule',
            terminal: false,
            templateUrl: '/static/templates/schedule-matches.html',
            transclude: true,
            replace: true,
            scope: {
                queryDate:    '=queryDate'
            },
            link: function($scope,$element,$attributes,ctrl) {
                console.log("Link scheduleMatches");

                var schedule_iterator = 1;

                $scope.match = {
                    'sets' : []
                };

                var update = function() {
                    TeamSchedule.get({'date' : $scope.queryDate,'ver' : schedule_iterator}, function(data) {
                        console.log("Returned the team schedule.. updating values.");
                        $scope.match.sets = data.match;
                        schedule_iterator += 1;
                    });
                };

                amplify.subscribe(tb.events.SCHED_UPDATED,function() {update();});

                $scope.$watch('queryDate',function(){
                    console.log("ScheduleMatches queryDate changed");
                    update();
                });

                $scope.pickTeams = function() {
                    console.log("Picking Teams for " + $scope.queryDate);
                    PickTeams.save({date: $scope.queryDate},function(data){
                        console.log("Done Picking Teams:" + data.status + " " + data.date);
                        update();
                    },function(data, e, stuff) {
                        console.log("Error Picking Teams:" + e);
                    });
                };

                update();
            }
        }
    }
]);

