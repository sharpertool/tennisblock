// set initial view and register event handlers
window.onload = function()
{
    document.getElementById('form_select').style.display = '';
    document.getElementById('form_fields').style.display = 'none';

    window.cal1 = new YAHOO.widget.Calendar("cal1", "calendar",
       { mindate: '1/1/2007',
       maxdate: '12/31/2015',
       title: 'Select Date',
       close: true 
       });
    window.cal1.selectEvent.subscribe(updatePostDate, cal1, true);
    YAHOO.util.Event.addListener("show_calendar", "click",
        window.cal1.show, window.cal1, true); 
    updateCalendar();
    document.getElementById('post_date').onchange = updateCalendar;

    document.getElementById('post_id').onchange = show_form;
    document.getElementById('form_submit').onclick = submit_form;
    document.getElementById('form_reset').onclick = reset_form;
    document.getElementById('delete').onclick = submit_warning;
}

// update the post_date field when the user changes the calendar's date
function updatePostDate(type,args,obj)
{
    var month = (args[0][0][1] < 10) ? '0' + args[0][0][1] : args[0][0][1];
    var day = (args[0][0][2] < 10) ? '0' + args[0][0][2] : args[0][0][2];
    var year = args[0][0][0];

    document.getElementById('post_date').value = month + '/' + day + '/' + year;
    window.cal1.hide();
}

// update the calendar's date when the user changes the post_date field
function updateCalendar()
{ 
    var field = document.getElementById('post_date'); 

    if (field.value)
    { 
        window.cal1.select(field.value); 
        var selectedDates = window.cal1.getSelectedDates(); 
        if (selectedDates.length > 0)
        { 
            var firstDate = selectedDates[0]; 
            window.cal1.cfg.setProperty('pagedate',
                (firstDate.getMonth() + 1) + '/' + firstDate.getFullYear()); 
        }
    } 
    window.cal1.render(); 
}

// unhide the form when the user choses to modify a page
function show_form()
{
    fetch_info();
    document.getElementById('form_select').style.display = 'none';
    document.getElementById('form_fields').style.display = '';
    if (document.getElementById('post_id').value == 'new')
    {
        document.getElementById('delete_field').style.display = 'none';
    }
    else
    {
        document.getElementById('delete_field').style.display = '';
    }
}

// confirm is user checked delete 
function submit_form()
{
    if (document.getElementById('delete').checked)
    {
        return confirm('Are you sure you wish to delete this entry?');
    }
}

// highlight the submit button if record will be deleted
function submit_warning()
{
    if (document.getElementById('delete').checked)
    {
        document.getElementById('form_submit').style.backgroundColor =
            '#FF9999';
    }
    else
    {
        document.getElementById('form_submit').style.backgroundColor = '';
    }    
}

// clear form
function reset_form()
{
    if (!confirm('Are you sure you wish to cancel?')) return false;

    document.getElementById('form_fields').style.display = 'none';
    document.getElementById('form_select').style.display = '';

    // manually clear the RTE area
    document.getElementById('post_text').value = '';
    tinyMCE.updateContent(tinyMCE.getInstanceById('mce_editor_0').formElement.id);

    // default action of reset button will clear fields and reset select index
    // so an explicit clearing is not needed so long as we return true to not
    // break that bubble
    return true;
}

// retrieve existing information via "AJAX" 
var httpObj;
function fetch_info()
{
    var select = document.getElementById('post_id');
    if (select.options[select.selectedIndex].value == 'new') 
    {
        return;
    }

    var url = 'fetch_admin.php?post_id=' +
         select.options[select.selectedIndex].value + "&nocache=" +
         (new Date()).getTime();

    httpObj = createXMLHTTPObject();
    httpObj.open('GET', url, true);
    httpObj.onreadystatechange = function()
    {
        // populate the fields
        if (httpObj.readyState == 4 && httpObj.responseText)
        {
            var r = eval('(' + httpObj.responseText + ')');

            document.getElementById('post_title').value = r.post_title;
            document.getElementById('post_date').value = r.post_date;
            updateCalendar();
            document.getElementById('post_text').value = r.post_text;
            tinyMCE.updateContent(tinyMCE.getInstanceById('mce_editor_0').formElement.id);
        }
    }
    httpObj.send(null);
}
