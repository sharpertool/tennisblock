/**
 * $Id: editor_template_src.js 162 2007-01-03 16:16:52Z spocke $
 *
 * @author Moxiecode
 * @copyright Copyright © 2004-2007, Moxiecode Systems AB, All rights reserved.
 */

/* Import theme specific language pack */
tinyMCE.importThemeLanguagePack('custom');


var TinyMCE_CustomTheme = {
	// List of button ids in tile map
	_buttonMap : 'bold,bullist,cleanup,italic,numlist,strikethrough',

	getEditorTemplate : function() {
		var html = '';

		html += '<table class="mceEditor" border="0" cellpadding="0" cellspacing="0" width="{$width}" height="{$height}">';
		html += '<tr><td align="center">';
		html += '<span id="{$editor_id}">IFRAME</span>';
		html += '</td></tr>';
		html += '<tr><td class="mceToolbar" align="center" height="1">';
		html += tinyMCE.getButtonHTML('bold', 'lang_bold_desc', '{$themeurl}/images/{$lang_bold_img}', 'Bold');
		html += tinyMCE.getButtonHTML('italic', 'lang_italic_desc', '{$themeurl}/images/{$lang_italic_img}', 'Italic');
		html += tinyMCE.getButtonHTML('strikethrough', 'lang_striketrough_desc', '{$themeurl}/images/strikethrough.gif', 'Strikethrough');
		html += '<img src="{$themeurl}/images/separator.gif" width="2" height="20" class="mceSeparatorLine" />';
		html += tinyMCE.getButtonHTML('bullist', 'lang_bullist_desc', '{$themeurl}/images/bullist.gif', 'InsertUnorderedList');
		html += tinyMCE.getButtonHTML('numlist', 'lang_numlist_desc', '{$themeurl}/images/numlist.gif', 'InsertOrderedList');
		html += '<img src="{$themeurl}/images/separator.gif" width="2" height="20" class="mceSeparatorLine" />';
		html += tinyMCE.getButtonHTML('link', 'lang_link_desc', '{$themeurl}/images/link.gif', 'mceLink');
		html += tinyMCE.getButtonHTML('unlink', 'lang_unlink_desc', '{$themeurl}/images/unlink.gif', 'unlink');
		html += tinyMCE.getButtonHTML('image', 'lang_image_desc', '{$themeurl}/images/image.gif', 'mceImage');
		html += '<img src="{$themeurl}/images/separator.gif" width="2" height="20" class="mceSeparatorLine" />';
		html += tinyMCE.getButtonHTML('cleanup', 'lang_cleanup_desc', '{$themeurl}/images/cleanup.gif', 'mceCleanup');
		html += tinyMCE.getButtonHTML('code', 'lang_theme_code_desc', '{$themeurl}/images/code.gif', 'mceCodeEditor');
		html += '</td></tr></table>';

		return {
			delta_width : 0,
			delta_height : 20,
			html : html
		};
	},

        // Theme specific execcommand handling.
        execCommand : function(editor_id, element, command, user_interface, value) {
                switch (command) {
                        case "mceCodeEditor":
                                var template = new Array();

                                template['file'] = 'source_editor.htm';
                                template['width'] = parseInt(tinyMCE.getParam("theme_custom_source_editor_width", 720));
                                template['height'] = parseInt(tinyMCE.getParam("theme_custom_source_editor_height", 580));

                                tinyMCE.openWindow(template, {editor_id : editor_id, resizable : "yes", scrollbars : "no", inline : "yes"});
                                return true;


                          case "mceLink":
                                var inst = tinyMCE.getInstanceById(editor_id);
                                var doc = inst.getDoc();
                                var selectedText = "";

                                if (tinyMCE.isMSIE) {
                                        var rng = doc.selection.createRange();
                                        selectedText = rng.text;
                                } else
                                        selectedText = inst.getSel().toString();

                                if (!tinyMCE.linkElement) {
                                        if ((tinyMCE.selectedElement.nodeName.toLowerCase() != "img") && (selectedText.length <= 0))
                                                return true;
                                }

                                var href = "", target = "", title = "", onclick = "", action = "insert", style_class = "";

                                if (tinyMCE.selectedElement.nodeName.toLowerCase() == "a")
                                        tinyMCE.linkElement = tinyMCE.selectedElement;

                                // Is anchor not a link
                                if (tinyMCE.linkElement != null && tinyMCE.getAttrib(tinyMCE.linkElement, 'href') == "")
                                        tinyMCE.linkElement = null;

                                if (tinyMCE.linkElement) {
                                        href = tinyMCE.getAttrib(tinyMCE.linkElement, 'href');
                                        target = tinyMCE.getAttrib(tinyMCE.linkElement, 'target');
                                        title = tinyMCE.getAttrib(tinyMCE.linkElement, 'title');
                                        onclick = tinyMCE.getAttrib(tinyMCE.linkElement, 'onclick');
                                        style_class = tinyMCE.getAttrib(tinyMCE.linkElement, 'class');

                                        // Try old onclick to if copy/pasted content
                                        if (onclick == "")
                                                onclick = tinyMCE.getAttrib(tinyMCE.linkElement, 'onclick');

                                        onclick = tinyMCE.cleanupEventStr(onclick);

                                        href = eval(tinyMCE.settings['urlconverter_callback'] + "(href, tinyMCE.linkElement, true);");

                                        // Use mce_href if defined
                                        mceRealHref = tinyMCE.getAttrib(tinyMCE.linkElement, 'mce_href');
                                        if (mceRealHref != "") {
                                                href = mceRealHref;


                                                if (tinyMCE.getParam('convert_urls'))
                                                        href = eval(tinyMCE.settings['urlconverter_callback'] + "(href, tinyMCE.linkElement, true);");
                                        }

                                        action = "update";
                                }

                                var template = new Array();

                                template['file'] = 'link.htm';
                                template['width'] = 310;
                                template['height'] = 200;

                                // Language specific width and height addons
                                template['width'] += tinyMCE.getLang('lang_insert_link_delta_width', 0);
                                template['height'] += tinyMCE.getLang('lang_insert_link_delta_height', 0);

                                if (inst.settings['insertlink_callback']) {
                                        var returnVal = eval(inst.settings['insertlink_callback'] + "(href, target, title, onclick, action, style_class);");
                                        if (returnVal && returnVal['href'])
                                                TinyMCE_AdvancedTheme._insertLink(returnVal['href'], returnVal['target'], returnVal['title'], returnVal['onclick'], returnVal['style_class']);
                                } else {
                                        tinyMCE.openWindow(template, {href : href, target : target, title : title, onclick : onclick, action : action, className : style_class, inline : "yes"});
                                }

                                return true;

                        case "mceImage":
                                var src = "", alt = "", border = "", hspace = "", vspace = "", width = "", height = "", align = "";
                                var title = "", onmouseover = "", onmouseout = "", action = "insert";
                                var img = tinyMCE.imgElement;
                                var inst = tinyMCE.getInstanceById(editor_id);

                                if (tinyMCE.selectedElement != null && tinyMCE.selectedElement.nodeName.toLowerCase() == "img") {
                                        img = tinyMCE.selectedElement;
                                        tinyMCE.imgElement = img;
                                }

                                if (img) {
                                        // Is it a internal MCE visual aid image, then skip this one.
                                        if (tinyMCE.getAttrib(img, 'name').indexOf('mce_') == 0)
                                                return true;

                                        src = tinyMCE.getAttrib(img, 'src');
                                        alt = tinyMCE.getAttrib(img, 'alt');

                                        // Try polling out the title
                                        if (alt == "")
                                                alt = tinyMCE.getAttrib(img, 'title');

                                        // Fix width/height attributes if the styles is specified
                                        if (tinyMCE.isGecko) {
                                                var w = img.style.width;
                                                if (w != null && w != "")
                                                        img.setAttribute("width", w);

                                                var h = img.style.height;
                                                if (h != null && h != "")
                                                        img.setAttribute("height", h);
                                        }

                                        border = tinyMCE.getAttrib(img, 'border');
                                        hspace = tinyMCE.getAttrib(img, 'hspace');
                                        vspace = tinyMCE.getAttrib(img, 'vspace');
                                        width = tinyMCE.getAttrib(img, 'width');
                                        height = tinyMCE.getAttrib(img, 'height');
                                        align = tinyMCE.getAttrib(img, 'align');
                                        onmouseover = tinyMCE.getAttrib(img, 'onmouseover');
                                        onmouseout = tinyMCE.getAttrib(img, 'onmouseout');
                                        title = tinyMCE.getAttrib(img, 'title');

                                        // Is realy specified?
 if (tinyMCE.isMSIE) {
                                                width = img.attributes['width'].specified ? width : "";
                                                height = img.attributes['height'].specified ? height : "";
                                        }

                                        //onmouseover = tinyMCE.getImageSrc(tinyMCE.cleanupEventStr(onmouseover));
                                        //onmouseout = tinyMCE.getImageSrc(tinyMCE.cleanupEventStr(onmouseout));

                                        src = eval(tinyMCE.settings['urlconverter_callback'] + "(src, img, true);");

                                        // Use mce_src if defined
                                        mceRealSrc = tinyMCE.getAttrib(img, 'mce_src');
                                        if (mceRealSrc != "") {
                                                src = mceRealSrc;

                                                if (tinyMCE.getParam('convert_urls'))
                                                        src = eval(tinyMCE.settings['urlconverter_callback'] + "(src, img, true);");
                                        }

                                        //if (onmouseover != "")
                                        //      onmouseover = eval(tinyMCE.settings['urlconverter_callback'] + "(onmouseover, img, true);");

                                        //if (onmouseout != "")
                                        //      onmouseout = eval(tinyMCE.settings['urlconverter_callback'] + "(onmouseout, img, true);");

                                        action = "update";
                                }

                                var template = new Array();

                                template['file'] = 'image.htm?src={$src}';
                                template['width'] = 355;
                                template['height'] = 265 + (tinyMCE.isMSIE ? 25 : 0);

                                // Language specific width and height addons
                                template['width'] += tinyMCE.getLang('lang_insert_image_delta_width', 0);
                                template['height'] += tinyMCE.getLang('lang_insert_image_delta_height', 0);

                                if (inst.settings['insertimage_callback']) {
                                        var returnVal = eval(inst.settings['insertimage_callback'] + "(src, alt, border, hspace, vspace, width, height, align, title, onmouseover, onmouseout, action);");
                                        if (returnVal && returnVal['src'])
                                                TinyMCE_AdvancedTheme._insertImage(returnVal['src'], returnVal['alt'], returnVal['border'], returnVal['hspace'], returnVal['vspace'], returnVal['width'], returnVal['height'], returnVal['align'], returnVal['title'], returnVal['onmouseover'], returnVal['onmouseout']);
                                } else
tinyMCE.openWindow(template, {src : src, alt : alt, border : border, hspace : hspace, vspace : vspace, width : width, height : height, align : align, title : title, onmouseover : onmouseover, onmouseout : onmouseout, action : action, inline : "yes"});

                                return true;
                }

                return false;
        },

        _insertImage : function(src, alt, border, hspace, vspace, width, height, align, title, onmouseover, onmouseout) {
                tinyMCE.execCommand("mceInsertContent", false, tinyMCE.createTagHTML('img', {
                        src : tinyMCE.convertRelativeToAbsoluteURL(tinyMCE.settings['base_href'], src), // Force absolute
                        mce_src : src,
                        alt : alt,
                        border : border,
                        hspace : hspace,
                        vspace : vspace,
                        width : width,
                        height : height,
                        align : align,
                        title : title,
                        onmouseover : onmouseover,
                        onmouseout : onmouseout
                }));
        },

        _insertLink : function(href, target, title, onclick, style_class) {

                if (tinyMCE.selectedInstance && tinyMCE.selectedElement && tinyMCE.selectedElement.nodeName.toLowerCase() == "img") {
                        var doc = tinyMCE.selectedInstance.getDoc();
                        var linkElement = tinyMCE.getParentElement(tinyMCE.selectedElement, "a");
                        var newLink = false;

                        if (!linkElement) {
                                linkElement = doc.createElement("a");
                                newLink = true;
                        }

                        var mhref = href;
                        var thref = eval(tinyMCE.settings['urlconverter_callback'] + "(href, linkElement);");
                        mhref = tinyMCE.getParam('convert_urls') ? href : mhref;

                        tinyMCE.setAttrib(linkElement, 'href', thref);
                        tinyMCE.setAttrib(linkElement, 'mce_href', mhref);
                        tinyMCE.setAttrib(linkElement, 'target', target);
                        tinyMCE.setAttrib(linkElement, 'title', title);
                        tinyMCE.setAttrib(linkElement, 'onclick', onclick);
                        tinyMCE.setAttrib(linkElement, 'class', style_class);

                        if (newLink) {
                                linkElement.appendChild(tinyMCE.selectedElement.cloneNode(true));
                                tinyMCE.selectedElement.parentNode.replaceChild(linkElement, tinyMCE.selectedElement);
                        }

                        return;
                }

                if (!tinyMCE.linkElement && tinyMCE.selectedInstance) {
                        if (tinyMCE.isSafari) {
                                tinyMCE.execCommand("mceInsertContent", false, '<a href="' + tinyMCE.uniqueURL + '">' + tinyMCE.selectedInstance.selection.getSelectedHTML() + '</a>');
                        } else
                                tinyMCE.selectedInstance.contentDocument.execCommand("createlink", false, tinyMCE.uniqueURL);

                        tinyMCE.linkElement = tinyMCE.getElementByAttributeValue(tinyMCE.selectedInstance.contentDocument.body, "a", "href", tinyMCE.uniqueURL);

                        var elementArray = tinyMCE.getElementsByAttributeValue(tinyMCE.selectedInstance.contentDocument.body, "a", "href", tinyMCE.uniqueURL);

                        for (var i=0; i<elementArray.length; i++) {
                                var mhref = href;
                                var thref = eval(tinyMCE.settings['urlconverter_callback'] + "(href, elementArray[i]);");
                                mhref = tinyMCE.getParam('convert_urls') ? href : mhref;

                                tinyMCE.setAttrib(elementArray[i], 'href', thref);
                                tinyMCE.setAttrib(elementArray[i], 'mce_href', mhref);
                                tinyMCE.setAttrib(elementArray[i], 'target', target);
                                tinyMCE.setAttrib(elementArray[i], 'title', title);
                                tinyMCE.setAttrib(elementArray[i], 'onclick', onclick);
                                tinyMCE.setAttrib(elementArray[i], 'class', style_class);
                        }

                        tinyMCE.linkElement = elementArray[0];
                }

                if (tinyMCE.linkElement) {
                        var mhref = href;
                        href = eval(tinyMCE.settings['urlconverter_callback'] + "(href, tinyMCE.linkElement);");
                        mhref = tinyMCE.getParam('convert_urls') ? href : mhref;

                        tinyMCE.setAttrib(tinyMCE.linkElement, 'href', href);
                        tinyMCE.setAttrib(tinyMCE.linkElement, 'mce_href', mhref);
                        tinyMCE.setAttrib(tinyMCE.linkElement, 'target', target);
                        tinyMCE.setAttrib(tinyMCE.linkElement, 'title', title);
                        tinyMCE.setAttrib(tinyMCE.linkElement, 'onclick', onclick);
                        tinyMCE.setAttrib(tinyMCE.linkElement, 'class', style_class);
                }
        },
 
	handleNodeChange : function(editor_id, node) {
		// Reset old states
		tinyMCE.switchClass(editor_id + '_bold', 'mceButtonNormal');
		tinyMCE.switchClass(editor_id + '_italic', 'mceButtonNormal');
		tinyMCE.switchClass(editor_id + '_strikethrough', 'mceButtonNormal');
		tinyMCE.switchClass(editor_id + '_bullist', 'mceButtonNormal');
		tinyMCE.switchClass(editor_id + '_numlist', 'mceButtonNormal');

		// Handle elements
		do {
			switch (node.nodeName.toLowerCase()) {
				case "b":
				case "strong":
					tinyMCE.switchClass(editor_id + '_bold', 'mceButtonSelected');
				break;

				case "i":
				case "em":
					tinyMCE.switchClass(editor_id + '_italic', 'mceButtonSelected');
				break;

				case "strike":
					tinyMCE.switchClass(editor_id + '_strikethrough', 'mceButtonSelected');
				break;
				
				case "ul":
					tinyMCE.switchClass(editor_id + '_bullist', 'mceButtonSelected');
				break;

				case "ol":
					tinyMCE.switchClass(editor_id + '_numlist', 'mceButtonSelected');
				break;
			}
		} while ((node = node.parentNode) != null);
	}
};
 
tinyMCE.addTheme("custom", TinyMCE_CustomTheme);
tinyMCE.addButtonMap(TinyMCE_CustomTheme._buttonMap);
