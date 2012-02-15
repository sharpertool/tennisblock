/**
 * Copyright: Aspen Labs, LLC. 2011
 * User: kutenai
 * Date: 1/9/12
 * Time: 7:19 PM
 */

$(document).ready(function() {
    initForms();
    do_restore_session();

    var listItems = $(".list_3 li");

    listItems.draggable({
        zIndex: 3000,
        appendTo: "#schematic",
        scroll: false,
        helper: function() {
        }
    });

    listItems.bind("drag", function(e, ui) {
        if(helper != null) {
            $(helper).remove();
            helper = null;
        }
        $(this).data('draggable').offset.click.top  = 0;
        $(this).data('draggable').offset.click.left = 0;
    });

    listItems.bind("dragstop", function(e, ui) {
        console.log("Drag stopped");
    });

    listItems.bind("click", function(e, ui) {
        if(helper != null) {
            $(helper).remove();
            helper = null;
        }

    });


};

function initForms() {
    addJQueryActions();

};

function do_restore_session() {

};

function addJQueryActions()
{
    $("#login").live("click", function() {
        do_login();
        return false;
    });
    $("#logout").live("click", function() {
        do_logout();
        return false;
    });

    // Help
    $("#help_button").click(function(e) {
        e.preventDefault();
        $("#help").dialog({
            title: "Scheme-it Help",
            resizable: false,
            modal: true,
            draggable: false,
            dialogClass: "graph-popup-dialog",
            width: 800,
            height: 435
        });
        $("#help_content").load($("#help_nav li:first-child a").attr("href"));
    });

    $("#help_nav a").click(function(e) {
        e.preventDefault();
        $("#help_content").load($(this).attr("href"));
        $("#help_nav a").toggleClass("hot", false);
        $(this).toggleClass("hot", true);
    });

    // Main Toolbar
    $("#toolbar_save").click(function() {
        if (!is_logged_in()) {
            do_login(this);
        } else {
            do_save();
        }
    });
};
