/**
 * Created with IntelliJ IDEA.
 * User: kutenai
 * Date: 8/13/12
 * Time: 9:57 PM
 * To change this template use File | Settings | File Templates.
 */

function GBGui() {

}

GBGui.prototype.init = function() {
    // --- Tabs on Top ----
    $("#sitenav li").hover(// Tab Hover Class
        function () {
            if (!$(this).hasClass('tab_hot')) {  // Don't dork with hot tab
                $(this).addClass('tab_hover');
            }
        },
        function () {
            $(this).removeClass('tab_hover');
        }
    );
};
