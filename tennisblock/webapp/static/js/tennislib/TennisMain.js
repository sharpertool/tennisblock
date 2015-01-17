/**
 * Created with IntelliJ IDEA.
 * User: kutenai
 * Date: 8/13/12
 * Time: 9:50 PM
 * To change this template use File | Settings | File Templates.
 */


$(document).ready(function() {

    tb.toggleMenu = function() {
        console.log("Toggling menu");
        $('#navigation ul').toggleClass('hide');
        $('#leftButton').toggleClass('pressed');
    }

});

