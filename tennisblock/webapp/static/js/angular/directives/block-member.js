/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 10/17/13
 * Time: 11:56 AM
 */

tennisblockapp.directive('blockMember',['Members','$q',
    function(Members,$q) {
        // Initialization

        return {
            priority: 10,
            restrict: 'EA',
            require: '^blockMembers',
            controller: 'MembersController',
            terminal: false,
            templateUrl: '/static/templates/block-member.html',
            transclude: true,
            replace: true,
            scope: {
                member : '='
            },
            link: function($scope,$element,$attributes,ctrl) {
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
                };

                $scope.memberFieldChanged = function(member,field) {
                    return member[field] != member.original[field];
                };

                $scope.updateMember = function(member) {
                    var mdef = $q.defer();
                    Members.save({},{'member':member},function() {
                        mdef.resolve();
                    });
                    mdef.promise.then(function() {
                        Members.get({id:member.id},function(data) {
                            var m = $scope.member;
                            delete m.original;
                            m.original = angular.copy(m);
                        });
                    });
                };

                $scope.updateBlockMember = function(member) {
                    Members.update({id:member.id},{'blockmember':member.blockmember});
                };

                $scope.insertNewMember = function(member) {
                    var mdef = $q.defer();
                    Members.insert({},{'member':member},function(data) {
                        mdef.resolve(data);
                    });
                    mdef.promise.then(function(data) {
                        var newid = data.id;
                        Members.get({id:newid },function(data) {
                            var m = $scope.member;
                            delete m.original;
                            m.new = false;
                            m.changed = false;
                            m.original = JSON.parse(JSON.stringify(m));
                        });
                    });
                };

                $scope.deleteNewMember = function(member) {
                    var mdef = $q.defer();
                    Members.remove({},{'member':member},function(data) {
                        mdef.resolve(data);
                    });
                    mdef.promise.then(function(data) {
                        console.log("Player actually removed!");
                        ctrl.deleteMember(member);
                    });
                };
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
                   field : '@',
                   member : '='
            },
            link: function($scope,$element,$attrs) {
                console.log("Link blockMemberItem");

                $scope.isChanged = function() {
                    var f = $scope.field;
                    var m = $scope.member;
                    return !m.new && m.original[f] != m[f];
                }
            }
        };
    }
]);
