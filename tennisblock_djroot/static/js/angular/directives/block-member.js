/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 10/17/13
 * Time: 11:56 AM
 */

tennisblockapp.directive('blockMember',[
    function() {
        // Initialization

        return {
            priority: 10,
            restrict: 'EA',
            terminal: false,
            templateUrl: '/static/templates/block-member.html',
            //transclude: true,
            replace: false,
            scope: {
                member : '='
            },
            link: function($scope,$element,$attributes) {
                console.log("Link blockMember");

                var attrs = ['first','last','gender','ntrp','microntrp','phone','email'];

                $scope.memberChanged = function(member) {
                    var changed = false;
                    var m = $scope.member;
                    _.each(attrs,function(attr) {
                        changed = changed || m[attr] != m.original[attr];
                    });
                    m.changed = changed;
                    return changed;
                }

                $scope.memberFieldChanged = function(member,field) {
                    return member[field] != member.original[field];
                }
            }
        };
    }
]);

tennisblockapp.directive('blockMemberItem',[
    function() {
        // Initialization

        return {
            priority: 10,
            restrict: 'EA',
            terminal: false,
            templateUrl: '/static/templates/block-member-item.html',
            //transclude: true,
            replace: true,
            scope: {
                member : '=',
                mvar : '='
            },
            link: function($scope,$element,$attrs) {
                console.log("Link blockMemberItem");

                var fld=$attrs['field'];
                $scope.field = $attrs['field'];

                $scope.isChanged = function() {
                    var changed = $scope.member[fld] != $scope.member.original[fld];
                    console.log("Field " + fld + " is changed:" + changed);
                    return changed;
                }
            }
        };
    }
]);
