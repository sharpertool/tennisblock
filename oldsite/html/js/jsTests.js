/**
 * Created by IntelliJ IDEA.
 * User: kutenai
 * Date: 12/5/11
 * Time: 12:13 PM
 * To change this template use File | Settings | File Templates.
 */

var editor;
var graph;
function eeParent(name) {

    this.name = name;
    this.f3 = function() {
        console.log("Parent this.f3");
    }

};

eeParent.prototype.f1 = function() {
    console.log('Parent f1');
}

eeParent.prototype.f2 = function() {
    console.log("Parent f2");
}

function eeChild(name,dad) {

    this.dad = dad;

    this.f3 = function() {
        console.log("Child this.f3");
    }

    eeParent.call(this,name);
}

//eeChild.prototype = eeParent.prototype;
var F = function() {};

F.prototype =
eeChild.prototype = new eeParent();
eeChild.prototype.constructor = eeChild;

eeChild.prototype.showFamily = function() {
    console.log("Dad:" + this.dad);
    console.log("Me:" + this.name);
}

$(document).ready(function()
{
    console.log("Test JS OnRead");

    Object.defineProperty(eeChild, 'newProp', { val: 'testing' } );


    var p = new eeParent('Ed');
    var c = new eeChild('Joel');

    Object.defineProperty(eeChild, 'newProp', { val: 'testing' } );

    console.log("Enumerate Parent");
    for (x in p) {
        console.log(x);
    }

    console.log("Enumerate Child");
    for (x in c) {
        console.log(x);
    }

    console.log(c.newProp);

    editor = new eeEditor();
    graph = editor.graph;

    console.log("Graph own properties:");
    for (prop in graph) {
        if (graph.hasOwnProperty(prop)){
            console.log("Own:" + prop);
        }
    }

    console.log("Graph inherited properties:");
    for (prop in graph) {
        if (!graph.hasOwnProperty(prop)){
            console.log("graph inherited:" + prop);
        }
    }

    console.log("Graph prototype properties:");
    for (prop in mxGraph.prototype) {
        console.log("mxGraph prototype:" + prop);
    }

});




