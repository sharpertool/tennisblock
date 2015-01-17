/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 10/19/13
 * Time: 5:56 PM
 */

tennisblockapp.controller( "MembersController",
    [ "$scope", "$attrs",
        function( $scope, $attrs ){
            this.members = {};

            /**
             * registerMembers
             *
             * Called by the members-list to give the controller
             * access to the members object.
             * @param mobj
             */
            this.registerMembers = function(mobj) {
                this.members = mobj;
            };

            /**
             * addNewMember
             *
             * Add a new member to the master contorllers list.
             * @param newMember
             */
            this.addNewMember = function(newMember) {
                console.log("Added a new member in the controller..");
                this.members.allmembers.push(newMember);
            };

            /**
             * Remove a member from the master list.
             *
             * The database backend stuff is all done elsewhere..
             * @param m
             */
            this.deleteMember = function(m) {
                console.log("Deleting new member..");
                this.members.allmembers = _.without(this.members.allmembers,m);
            };
        } ] );


