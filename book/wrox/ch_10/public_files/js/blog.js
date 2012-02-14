// toggle the comments display of a particular post
function toggleComments(id, link)
{
    var div = document.getElementById('comments_' + id);

    if (div.style.display == 'none')
    {
        link.innerHTML = 'Hide Comments';
        fetchComments(id);
        div.style.display = '';
    }
    else
    {
        link.innerHTML = 'Show Comments';
        div.style.display = 'none';
    }
}

// retrieve existing comments via "AJAX" 
window.httpObj;
function fetchComments(id)
{
    var div = document.getElementById('comments_' + id);

    var url = 'fetch.php?post_id=' + id + "&nocache=" + 
        (new Date()).getTime();

    window.httpObj = createXMLHTTPObject();
    window.httpObj.open('GET', url , true);
    window.httpObj.onreadystatechange = function()
    {
        // populate the fields
        if (window.httpObj.readyState == 4 && httpObj.responseText)
        {
            div.innerHTML = httpObj.responseText;
        }
    }
    window.httpObj.send(null);
}

// submit a comment via "AJAX"
function postComment(id, form)
{
    var url = form.action + "&nocache=" + (new Date()).getTime();
    var data = 'person_name=' + escape(form.person_name.value) +
        '&post_comment=' + escape(form.post_comment.value);

    window.httpObj = createXMLHTTPObject();
    window.httpObj.open('POST', url , true);
    window.httpObj.setRequestHeader('Content-type',
        'application/x-www-form-urlencoded');
    window.httpObj.setRequestHeader('Content-length', data.length);
    window.httpObj.setRequestHeader('Connection', 'close');

    window.httpObj.onreadystatechange = function()
    {
        // populate the fields
        if (window.httpObj.readyState == 4 && window.httpObj.responseText)
        {
            if (window.httpObj.responseText == 'OK')
            {
                fetchComments(id);
            }
            else
            {
                alert('Error posting comment.');
            }
        }
    }
    window.httpObj.send(data);
    return false;
}

