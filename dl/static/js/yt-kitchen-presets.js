// save new preset
$(document).on('click', '.configs-panel .save-button', function (e) {
    
    var obj = {
        'name': $("#config-name").val(),
        'config': $("#config").val()
    }
    var jsonObj = JSON.stringify(obj)

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/savepreset",
        headers:{'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        data: jsonObj,
        cahce: true,
        success: function (result) {
            
        },
        contentType: 'application/json',
        dataType: 'json',                
    });

    var row = $(`.name[data-name="${obj['name']}"]`)
    if (row.length > 0){
        row.closest('tr').children('.value').html(obj['config'])
    }
    else{
        var new_row = $('#row').html()
        new_row = new_row.replace('<td class="name" data-name=""></td>', `<td class="name" data-name="">${obj['name']}</td>`)
        new_row = new_row.replace(`data-name=""`, `data-name="${obj['name']}"`)
        new_row = new_row.replace('<td class="value"></td>', `<td class="value">${obj['config']}</td>`)

        $('table.data').append(new_row)
    }
});

// delete preset
$(document).on('click', '.delete', function (e) {
    
    var obj = {
        'name': $(this).closest('tr').children('.name').text()
    }
    var jsonObj = JSON.stringify(obj)

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/deletepreset",
        headers:{'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        data: jsonObj,
        cahce: true,
        success: function (result) {
            
        },
        contentType: 'application/json',
        dataType: 'json',                
    });

    $(this).closest('tr').remove()
});

// edit preset
$(document).on('click', '.edit', function (e) {
    
    $("#config-name").val($(this).closest('tr').children('.name').text())
    $("#config").val($(this).closest('tr').children('.value').text())

});