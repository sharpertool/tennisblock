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

    var zpad = function(num, size) {
        var s = "0" + num;
        return s.substr(s.length-size);
    };

    TennisUtils.prototype.pyDate2js = function(pydate) {
        if (typeof pydate === 'string') {
            var ymd = String(pydate).split('-');
            if (ymd.length == 3) {
                var y = ymd[0];
                var m = ymd[1]-1;
                var d = ymd[2];
                var jsdate = new Date(y, m,d);
                return jsdate;
            }
        }
        return pydate;
    };

    TennisUtils.prototype.jsDate2py = function(jsdate) {
        var d = new Date(jsdate);
        var pydate = d.getFullYear() + '-' + zpad(d.getMonth()+1,2) + '-' + d.getDate();
        return pydate;
    };


    tb.utils = new TennisUtils();

})();


