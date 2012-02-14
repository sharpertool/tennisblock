// register event handlers and set initial view
window.onload = function()
{
    document.getElementById('cat_delete').onclick = warnCategoryDelete;
    document.getElementById('cat_cancel').onclick = resetCategoryForm;
    document.getElementById('cat_submit').onclick = submitCategoryForm;

    document.getElementById('item_delete').onclick = warnItemDelete;
    document.getElementById('item_cancel').onclick = resetItemForm;
    document.getElementById('item_submit').onclick = submitItemForm;

    resetCategoryForm();
}

// reset the category form
function resetCategoryForm()
{
    // make sure all controls are enabled
    document.getElementById('cat_name').disabled = false;
    document.getElementById('cat_delete').disabled = false;
    document.getElementById('cat_submit').disabled = false;
    document.getElementById('cat_cancel').disabled = false;

    // hide sub forms
    document.getElementById('cat_form_tbl').style.display = 'none';
    document.getElementById('item_select_tbl').style.display = 'none';
    document.getElementById('item_form_tbl').style.display = 'none';

    // reset the submit button's background color and the delete option
    document.getElementById('cat_delete').checked = false;
    document.getElementById('cat_submit').style.backgroundColor = '';

    // populate the category select list and make visible
    retrieveCategorySelect();
    document.getElementById('cat_select_tbl').style.display = '';
}

// populate the category select list via AJAX
function retrieveCategorySelect()
{
    var url = 'inventory_process.php?retrieve_category_select&nocache=' +
        (new Date()).getTime();

    window.httpObj = createXMLHTTPObject();
    window.httpObj.onreadystatechange = function()
    {
        if (window.httpObj.readyState == 4)
        {
            document.getElementById('cat_select_cell').innerHTML =
                window.httpObj.responseText;

            // assign select list's event handler 
            document.getElementById('cat_select').onchange = showCategoryForms;
        }
    }

    window.httpObj.open('GET', url, false);
    window.httpObj.send(null);
}

// display the category's form and possibly a synced item list
function showCategoryForms()
{
    // hide the category select list
    document.getElementById('cat_select_tbl').style.display = 'none';

    var select = document.getElementById('cat_select');
    retrieveCategoryValues(select.options[select.selectedIndex].value);

    if (select.options[select.selectedIndex].value != 'new')
    {
        // populate the item list for this category and make visible
        retrieveItemSelect(select.options[select.selectedIndex].value);
        document.getElementById('item_select_tbl').style.display = '';
    }

    document.getElementById('cat_form_tbl').style.display = '';
}

// populate the category form via AJAX
function retrieveCategoryValues(value)
{
    if (value == 'new')
    {
        // clear fields if creating a new record
        document.getElementById('cat_name').value = '';
        document.getElementById('cat_delete_row').style.display = 'none';
    }
    else
    {
        var url = 'inventory_process.php?retrieve_category&id=' + value + 
            '&nocache=' + (new Date()).getTime();

        window.httpObj = createXMLHTTPObject();
        window.httpObj.onreadystatechange = function()
        {
            if (window.httpObj.readyState == 4)
            {
                var r = eval('(' + window.httpObj.responseText + ')');
                document.getElementById('cat_name').value = r.cat_name;
                document.getElementById('cat_delete_row').style.display = '';
            }
        }

        window.httpObj.open('GET', url, false);
        window.httpObj.send(null);
    }
}

// highlight the submit button if it will cause records to be deleted
function warnCategoryDelete()
{
    var btn = document.getElementById('cat_submit');
    if (document.getElementById('cat_delete').checked)
    {
        btn.style.backgroundColor = '#FF0000';
    }
    else
    {
        btn.style.backgroundColor = '';
    }
}

// submit the category form via AJAX
function submitCategoryForm()
{
    // warn if the submit will cause records to be deleted
    if (document.getElementById('cat_delete').checked)
    {
        if (!confirm('Deleting a category will delete the inventory items ' +
            'it contains as well.  Are you sure you wish to proceed?'))
        {
            return;
        }
    }

    // prepare the url and data
    var url = 'inventory_process.php?save_category&nocache=' +
        (new Date()).getTime(); 

    var select = document.getElementById('cat_select');
    var data = 'id=' + select.options[select.selectedIndex].value +
        '&name=' + escape(document.getElementById('cat_name').value);

    if (document.getElementById('cat_delete').checked)
    {
        data += '&delete=true';
    }

    window.httpObj = createXMLHTTPObject();
    window.httpObj.onreadystatechange = function()
    {
        if (window.httpObj.readyState == 4)
        {
            // reset the form when submission is complete
            resetCategoryForm();
        }
    }

    // set headers and send content
    window.httpObj.open('POST', url, false);
    window.httpObj.setRequestHeader('Content-type',
        'application/x-www-form-urlencoded');
    window.httpObj.setRequestHeader('Content-length', data.length);
    window.httpObj.setRequestHeader('Connection', 'close');
    window.httpObj.send(data);
}

// reset the item form
function resetItemForm()
{
    // make sure all category controls are disable
    document.getElementById('cat_name').disabled = true;
    document.getElementById('cat_delete').disabled = true;
    document.getElementById('cat_submit').disabled = true;
    document.getElementById('cat_cancel').disabled = true;

    // hide sub form
    document.getElementById('item_form_tbl').style.display = 'none';

    // reset the submit button's background color and the delete option
    document.getElementById('item_delete').checked = false;
    document.getElementById('item_submit').style.backgroundColor = '';

    // populate the item list and make it visible
    var select = document.getElementById('cat_select');
    retrieveItemSelect(select.options[select.selectedIndex].value);
    document.getElementById('item_select_tbl').style.display = '';
}

// populate the item select list for the selected category via AJAX
function retrieveItemSelect(id)
{
    var url = 'inventory_process.php?retrieve_item_select&id=' + id +
        '&nocache=' + (new Date()).getTime();

    window.httpObj = createXMLHTTPObject();
    window.httpObj.onreadystatechange = function()
    {
        if (window.httpObj.readyState == 4)
        {
            document.getElementById('item_select_cell').innerHTML =
                window.httpObj.responseText;

            // assign select list's event handler
            document.getElementById('item_select').onchange = showItemForm;
        }
    }

    window.httpObj.open('GET', url, false);
    window.httpObj.send(null);
}

// display the item's form
function showItemForm()
{
    var select = document.getElementById('item_select');

    // populate the item list for this category and make visible
    retrieveItemValues(select.options[select.selectedIndex].value);

    // hide item select list and make item form visible
    document.getElementById('item_select_tbl').style.display = 'none';
    document.getElementById('item_form_tbl').style.display = '';
    document.getElementById('item_submit').style.backgroundColor = '';
}

// populate the item form via AJAX
function retrieveItemValues(value)
{
    if (value == 'new')
    {
        // clear fields if creating a new record
        document.getElementById('item_name').value = '';
        document.getElementById('item_description').value = '';
        document.getElementById('item_price').value = '';
        document.getElementById('item_image').value = '';
        document.getElementById('item_delete_row').style.display = 'none';
    }
    else
    {
        var url = 'inventory_process.php?retrieve_item&id=' + value + 
            '&nocache=' + (new Date()).getTime();

        window.httpObj = createXMLHTTPObject();
        window.httpObj.onreadystatechange = function()
        {
            if (window.httpObj.readyState == 4)
            {
                var r = eval('(' + window.httpObj.responseText + ')');
                document.getElementById('item_name').value = r.item_name;
                document.getElementById('item_description').value = 
                    r.item_description;
                document.getElementById('item_price').value = r.item_price;
                document.getElementById('item_image').value = r.item_image;
                document.getElementById('item_delete_row').style.display = '';
            }
        }

        window.httpObj.open('GET', url, false);
        window.httpObj.send(null);
    }
}

// highlight the submit button if it will cause records to be deleted
function warnItemDelete()
{
    var btn = document.getElementById('item_submit');
    if (document.getElementById('item_delete').checked)
    {
        btn.style.backgroundColor = '#FF0000';
    }
    else
    {
        btn.style.backgroundColor = '';
    }
}

// submit the item form via AJAX
function submitItemForm()
{
    // warn if the submit will cause records to be deleted
    if (document.getElementById('item_delete').checked)
    {
        if (!confirm('You are about to delete an inventory item.  ' +
            'Are you sure you wish to proceed?'))
        {
            return;
        }
    }

    // prepare the url and data
    var url = 'inventory_process.php?save_item&nocache=' +
        (new Date()).getTime();

    var i_select = document.getElementById('item_select');
    var c_select = document.getElementById('cat_select');
    var data = 'id=' + i_select.options[i_select.selectedIndex].value +
        '&name=' + escape(document.getElementById('item_name').value) +
        '&description=' +
            escape(document.getElementById('item_description').value) +
        '&price=' + document.getElementById('item_price').value +
        '&image=' + escape(document.getElementById('item_image').value) +
        '&cat_id=' + c_select.options[c_select.selectedIndex].value;

    if (document.getElementById('item_delete').checked)
    {
        data += '&delete=true';
    }

    window.httpObj = createXMLHTTPObject();
    window.httpObj.onreadystatechange = function()
    {
        if (window.httpObj.readyState == 4)
        {
            // reset the form when submission is complete
            resetItemForm();
        }
    }

    // set headers and send content
    window.httpObj.open('POST', url, false);
    window.httpObj.setRequestHeader('Content-type',
        'application/x-www-form-urlencoded');
    window.httpObj.setRequestHeader('Content-length', data.length);
    window.httpObj.setRequestHeader('Connection', 'close');
    window.httpObj.send(data);
}