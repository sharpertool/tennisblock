/**
 * Created with IntelliJ IDEA.
 * User: kutenai
 * Date: 8/13/12
 * Time: 9:50 PM
 * To change this template use File | Settings | File Templates.
 */


$(document).ready(function() {

    // Initialize the jwplayer api key.. this is the key we paid for.
    if (typeof jwplayer !== 'undefined') {
        //jwplayer.key="fYnRtGDQRvdjBsT9eDoZz2vVaRWplQ67uT2nl5y4lIw=";
    }

    gb.log = log4javascript.getLogger();

    if (typeof less !== 'undefined') {
        less.env = 'development';
        less.optimization = 0;
        less.watch();
        less.refresh(true);
    }

    var popUpAppender = new log4javascript.PopUpAppender();
    var popUpLayout = new log4javascript.PatternLayout("%d{HH:mm:ss} %-5p - %m%n");
    popUpAppender.setLayout(popUpLayout);
    //log.addAppender(popUpAppender);

    gb.log.info("Initializing GardenBuzz on " + location.host);

    gb.gui = new GBGui();

    gb.gui.init();

    //$(window).resize(function() { gb.utils.onResize(); });

    //gb.utils.onResize();

    GardenBuzz.toggleMenu = function() {
        console.log("Toggling menu");
        $('#navigation ul').toggleClass('hide');
        $('#leftButton').toggleClass('pressed');
    }

});

