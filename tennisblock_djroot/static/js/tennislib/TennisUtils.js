/**
 * Created with IntelliJ IDEA.
 * User: kutenai
 * Date: 8/13/12
 * Time: 10:01 PM
 * To change this template use File | Settings | File Templates.
 */


(function() {

    function TennisUtils() {

    }

    TennisUtils.prototype.getBrowserWidth = function() {
        if (window.innerWidth){
            return window.innerWidth;}
        else if (document.documentElement && document.documentElement.clientWidth != 0){
            return document.documentElement.clientWidth;    }
        else if (document.body){return document.body.clientWidth;}
        return 0;
    };

    TennisUtils.prototype.getBrowserHeight = function() {
        if (window.innerHeight){
            return window.innerHeight;}
        else if (document.documentElement && document.documentElement.clientHeight != 0){
            return document.documentElement.clientHeight;    }
        else if (document.body){return document.body.clientHeight;}
        return 0;
    }

    TennisUtils.prototype.onResize = function() {
        return;
        var browserWidth = this.getBrowserWidth();
        var browserHeight = this.getBrowserHeight();

        var tb= $('#top_banner');

        var dyn = $('.dynamic');
        if (browserHeight < 800) {
            dyn.addClass('short');
        } else {
            dyn.removeClass('short');
        }


        dyn.removeClass('narrow');
        dyn.removeClass('wide');
        if (browserWidth < 1000) { // like 768 or something.
            dyn.addClass('narrow');
        } else if (browserWidth < 1280) {
            //dyn.addClass('width-med');
        } else {
            dyn.addClass('wide');
        }
    }

    tb.utils = new TennisUtils();

})();


