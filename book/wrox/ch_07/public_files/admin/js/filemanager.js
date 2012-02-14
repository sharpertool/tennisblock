/* retrieve all elements of a given class */
function getElementsByClass(search)
{
    var classElements = new Array();
    var els = document.getElementsByTagName('*');
    var pattern = new RegExp('(^|\\s)' + search + '(\\s|$)');

    for (var i = 0, j = 0; i < els.length; i++)
    {
        if (pattern.test(els[i].className))
        {
            classElements[j] = els[i];
            j++;
        }
    }
    
    return classElements;
}

/* create an XML HTTP Request object for "ajax" calls */
function createXMLHTTPObject()
{
    if (typeof XMLHttpRequest != 'undefined')
    {
        return new XMLHttpRequest();
    }
    else if (window.ActiveXObject)
    {
        var vers = [
            'Microsoft.XmlHttp',
            'MSXML2.XmlHttp',
            'MSXML2.XmlHttp.3.0',
            'MSXML2.XmlHttp.4.0',
            'MSXML2.XmlHttp.5.0'
        ];

        for (var i = vers.length - 1; i >= 0; i--)
        {
            try
            {
                httpObj = new ActiveXObject(vers[i]);
                return httpObj;
            }
            catch(e) {}
        }
    }
    throw new Error('XMLHTTP not supported');
}

// make loading feedback icon visible
function showLoader()
{
    document.getElementById('loading_icon').style.display = '';
}

// hide loading feedback icon 
function hideLoader()
{
    document.getElementById('loading_icon').style.display = 'none';
}

// register event handlers and set initial view
window.onload = function()
{
    document.getElementById('btn_open').onclick = openSelected;

    document.getElementById('btn_new_folder').onclick = showNewFolder;
    document.getElementById('form_new_submit').onclick = doNewFolder;
    document.getElementById('form_new_reset').onclick = hideForms;

    document.getElementById('btn_rename_file').onclick = showRenameFile;
    document.getElementById('form_rename_submit').onclick = doRenameFile;
    document.getElementById('form_rename_reset').onclick = hideForms;

    document.getElementById('btn_delete_file').onclick = doDeleteFile;

    document.getElementById('btn_upload_file').onclick = showUploadFile;
    document.getElementById('form_upload').target = 'my_iframe';
    document.getElementById('form_upload_submit').onclick = doUploadFile;
    document.getElementById('form_upload_reset').onclick = hideForms;

    window.directory = '/';  // current directory viewed
    refreshFilesList();
}

// mark a row selected and activate edit icons
function selectTableRow(data, e)
{
    // clear all previously selected rows and set this row as selected
    unselectTableRow();
    e.type = e.className;
    e.className = 'selectedRow';
    window.filename = data;
}

// unselect row
function unselectTableRow()
{
    // clear all previously selected rows
    for (i = 0, s = getElementsByClass('selectedRow'); i < s.length; i++)
    {
        s[i].className = s[i].type;
    }

    hideForms();
}

// highlight a row of the table for mouseover
function highlightTableRow(e)
{
    if (e.className != 'selectedRow')
    {
        e.style.backgroundColor = '#C3C3FE';
    }
}

// remove highlighting from the table row
function unhighlightTableRow(e)
{
    e.style.backgroundColor = '';
}

// retrieve display of existing files via "AJAX" 
function refreshFilesList()
{
    hideForms();

    var url = 'process.php?action=list&dir=' + window.directory + '&nocache=' +
        (new Date()).getTime();

    httpObj = createXMLHTTPObject();
    httpObj.open('GET', url , true);

    httpObj.onreadystatechange = function()
    {
        if (httpObj.readyState == 4 && httpObj.responseText)
        {
            // populate the fields
            document.getElementById('file_datagrid').innerHTML = 
                httpObj.responseText;

            window.filename = '';  // selected file
        }
    }
    httpObj.send(null);
}

// hide editing forms
function hideForms()
{
    document.getElementById('form_new').style.display = 'none';
    document.getElementById('form_rename').style.display = 'none';
    document.getElementById('form_upload').style.display = 'none';
}

// delete a directory or file via "AJAX"
function doDeleteFile()
{
    // don't delete a parent directory or if no file is selected 
    if (window.filename == '..' || window.filename == '')
    {
        return;
    }

    if (!confirm('Are you sure you wish to delete?'))
    {
        return;
    }
    var url = 'process.php?action=delete&dir=' + window.directory + '&file=' +
        window.filename + '&nocache=' + (new Date()).getTime();

    httpObj = createXMLHTTPObject();
    httpObj.open('GET', url , true);

    httpObj.onreadystatechange = function()
    {
        if (httpObj.readyState == 4 && httpObj.responseText)
        {
            if (httpObj.responseText == 'ok')
            {
                refreshFilesList();
            }
            else
            {
                alert('Unable to delete.');
            }
        }
    }
    httpObj.send(null);
}

// show form to create a new folder
function showNewFolder()
{
    hideForms();
    document.getElementById('form_new_name').value = '';
    document.getElementById('form_new').style.display = '';
}

// create a new folder via "AJAX"
function doNewFolder()
{
    var url = 'process.php?action=new&dir=' + window.directory + '&name=' +
        document.getElementById('form_new_name').value + '&nocache=' +
        (new Date()).getTime();

    httpObj = createXMLHTTPObject();
    httpObj.open('GET', url , true);

    httpObj.onreadystatechange = function()
    {
        if (httpObj.readyState == 4 && httpObj.responseText)
        {
            if (httpObj.responseText == 'ok')
            {
                refreshFilesList();
            }
            else
            {
                alert('Unable to create.');
            }
        }
    }
    httpObj.send(null);
    return false;
}

// show form to rename a folder or file
function showRenameFile()
{
    // don't rename a parent directory or if no file is selected
    if (window.filename == '..' || window.filename == '')
    {
        return;
    }

    hideForms();
    document.getElementById('form_rename_name').value = window.filename;
    document.getElementById('form_rename').style.display = '';
}

// rename a folder or file via "AJAX"
function doRenameFile()
{
    var url = 'process.php?action=rename&dir=' + window.directory + 
        '&oldfile=' + window.filename + '&newfile=' + 
        document.getElementById('form_rename_name').value + '&nocache=' +
        (new Date()).getTime();

    httpObj = createXMLHTTPObject();
    httpObj.open('GET', url , true);

    httpObj.onreadystatechange = function()
    {
        if (httpObj.readyState == 4 && httpObj.responseText)
        {
            if (httpObj.responseText == 'ok')
            {
                refreshFilesList();
            }
            else
            {
                alert('Unable to rename.');
            }
        }
    }
    httpObj.send(null);
    return false;
}

// show form to upload a new file 
function showUploadFile()
{
    hideForms();
    document.getElementById('form_upload').reset();
    document.getElementById('form_upload').style.display = '';
}

// upload a new file via "AJAX"
function doUploadFile()
{
    document.getElementById('form_upload_directory').value = window.directory;
}

// download the selected file or traverse into the selected directory
function openSelected()
{
    var url = 'process.php?action=open&dir=' + window.directory + '&file=' +
        window.filename + '&nocache=' + (new Date()).getTime();

    httpObj = createXMLHTTPObject();
    httpObj.open('GET', url , true);

    httpObj.onreadystatechange = function()
    {
        if (httpObj.readyState == 4 && httpObj.responseText)
        {
            var result = eval('(' + httpObj.responseText + ')');
            if (result.retType == 'directory')
            {
                window.directory = result.directory;
                refreshFilesList();
            }
            else if (result.retType == 'file')
            {
                window.location = 'download.php?&dir=' + window.directory +
                    '&file=' + window.filename + '&nocache=' +
                    (new Date()).getTime();
            }
            else
            {
                alert('Unknown error.');
            }
        }
    }
    httpObj.send(null);
    return false;
}

function uploadComplete()
{
    refreshFilesList();
}


