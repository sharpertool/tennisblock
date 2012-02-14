// retrieve all elements of a given class
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

// mark a row as selected
function selectTableRow(data, e)
{
    unselectTableRow();
    e.type = e.className;
    e.className = 'selectedRow';
    window.filename = data;
}

// unselect row
function unselectTableRow()
{
    for (i = 0, s = getElementsByClass('selectedRow'); i < s.length; i++)
    {
        s[i].className = s[i].type;
    }

    hideForms();
}

// highlight a table row on mouseover
function highlightTableRow(e)
{
    if (e.className != 'selectedRow')
    {
        e.style.backgroundColor = '#C3C3FE';
    }
}

// remove the highlighting on mouseout
function unhighlightTableRow(e)
{
    e.style.backgroundColor = '';
}

// register event handlers and set initial view
window.onload = function()
{
    window.directory = '/';  // current directory viewed
    window.filename = '';    // currently selected file

    // event handlers
    document.getElementById('btn_open').onclick = openSelected;

    document.getElementById('btn_new_folder').onclick = showNewFolder;
    document.getElementById('form_new_submit').onclick = doNewFolder;
    document.getElementById('form_new_reset').onclick = hideForms;

    document.getElementById('btn_upload').onclick = showUploadFile;
    document.getElementById('form_upload').target = 'my_iframe';
    document.getElementById('form_upload_submit').onclick = doUploadFile;
    document.getElementById('form_upload_reset').onclick = hideForms;

    document.getElementById('btn_rename').onclick = showRename;
    document.getElementById('form_rename_submit').onclick = doRename;
    document.getElementById('form_rename_reset').onclick = hideForms;

    document.getElementById('btn_delete').onclick = doDelete;

    // load the file listing
    refreshFilesList();
}

// retrieve display of files and directories
function refreshFilesList()
{
    hideForms();

    var url = 'process.php?action=list&dir=' + window.directory + '&nocache=' +
        (new Date()).getTime();

    window.httpObj = createXMLHTTPObject();
    window.httpObj.open('GET', url , true);

    window.httpObj.onreadystatechange = function()
    {
        if (window.httpObj.readyState == 4 && window.httpObj.responseText)
        {
            // populate the fields
            document.getElementById('file_datagrid').innerHTML =
                window.httpObj.responseText;

            window.filename = '';  // selected file
        }
    }

    window.httpObj.send(null);
}

// hide all input forms
function hideForms()
{
    document.getElementById('form_new').style.display = 'none';
    document.getElementById('form_rename').style.display = 'none';
    document.getElementById('form_upload').style.display = 'none';
}

// alert user the upload failed
function uploadFailed()
{
    alert('Failed to upload file.');
    hideForms();
}

// show form to upload a new file 
function showUploadFile()
{
    hideForms();
    document.getElementById('form_upload').reset();
    document.getElementById('form_upload').style.display = '';
}

// set form_upload_directory (allow browser to handle form
// submission)
function doUploadFile()
{
    document.getElementById('form_upload_directory').value = window.directory;
}

// show form to create new folder
function showNewFolder()
{
    hideForms();
    document.getElementById('form_new_name').value = '';
    document.getElementById('form_new').style.display = '';
}

// create a new folder
function doNewFolder()
{
    var url = 'process.php?action=new&dir=' + window.directory + '&name=' +
        document.getElementById('form_new_name').value + '&nocache=' +
        (new Date()).getTime();

    window.httpObj = createXMLHTTPObject();
    window.httpObj.open('GET', url , true);

    window.httpObj.onreadystatechange = function()
    {
        if (window.httpObj.readyState == 4 && window.httpObj.responseText)
        {
            if (window.httpObj.responseText == 'OK')
            {
                refreshFilesList();
            }
            else
            {
                alert('Unable to create directory.');
            }
        }
    }

    window.httpObj.send(null);
    return false;
}

// show form to rename a file or directory
function showRename()
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

// rename the file or directory
function doRename()
{
    var url = 'process.php?action=rename&dir=' + window.directory +
        '&oldfile=' + window.filename + '&newfile=' +
        document.getElementById('form_rename_name').value + '&nocache=' +
        (new Date()).getTime();

    window.httpObj = createXMLHTTPObject();
    window.httpObj.open('GET', url , true);

    window.httpObj.onreadystatechange = function()
    {
        if (window.httpObj.readyState == 4 && window.httpObj.responseText)
        {
            if (window.httpObj.responseText == 'OK')
            {
                refreshFilesList();
            }
            else
            {
                alert('Unable to rename entry.');
            }
        }
    }

    window.httpObj.send(null);
    return false;
}

// delete a directory or file
function doDelete()
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

    window.httpObj = createXMLHTTPObject();
    window.httpObj.open('GET', url , true);

    window.httpObj.onreadystatechange = function()
    {
        if (window.httpObj.readyState == 4 && window.httpObj.responseText)
        {
            if (window.httpObj.responseText == 'OK')
            {
                refreshFilesList();
            }
            else
            {
                alert('Unable to delete entry.');
            }
        }
    }

    httpObj.send(null);
}

// download the selected file or traverse into the selected directory
function openSelected()
{
    var url = 'process.php?action=open&dir=' + window.directory + '&file=' +
        window.filename + '&nocache=' + (new Date()).getTime();

    window.httpObj = createXMLHTTPObject();
    window.httpObj.open('GET', url , true);

    window.httpObj.onreadystatechange = function()
    {
        if (window.httpObj.readyState == 4 && window.httpObj.responseText)
        {
            var result = eval('(' + window.httpObj.responseText + ')');
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

    window.httpObj.send(null);
    return false;
}
