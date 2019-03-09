function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))
}

$(document).ready(function() {
  var csrftoken = Cookies.get('csrftoken')
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken)
      }
    }
  })
  
  $('#player_table input').on('change', function() {
    console.log('Changed:', $(this).val())
    console.log($(this).is(':checked'))
    console.log($(this))
    const id = $(this).val()
    const blockmember = $(this).is(':checked')
    const url = '/api/members/:id'
    $.ajax({
        type: "POST",
        url: url.replace(':id', id),
        data: {id: id, blockmember: blockmember}
      }
    ).then(function(result) {
      console.log('done')
      console.dir(result)
    })
  })
  
  $('button.delete-member').on('click', function() {
    const btn = $(this)
    const id = btn.attr('data-id')
    console.log('Deleting block member with id ', id)
    
    $.ajax({
        type: "DELETE",
        url: url.replace(':id', id),
      }
    ).then(function(result) {
      console.log('done')
      console.dir(result)
    })
    
  })
})
