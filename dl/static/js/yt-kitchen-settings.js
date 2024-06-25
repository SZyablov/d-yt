// save new settings
$(document).on('click', '.settings-panel .save-button', function (e) {
 
    var obj = {
        'destination_folder': $("#destination-folder").val(),
        'embed_thumbnail': $("#embed-thumbnail").is(":checked"),
        'embed_subtitles': $("#embed-subtitles").is(":checked"),
        'subtitle_langs': $("#subtitle-langs").val(),
        'embed_chapters': $("#embed-chapters").is(":checked"),
        'embed_metadata': $("#embed-metadata").is(":checked"),
        'embed_json_info': $("#embed-json-info").is(":checked")
    }
    var jsonObj = JSON.stringify(obj)

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/settingschange",
        headers:{'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        data: jsonObj,
        cahce: true,
        success: function (result) {
            
            $("#check").removeClass('hidden')
            setTimeout(function() {
                $("#check").addClass('hidden')
            }, 2000);            
            
        },
        contentType: 'application/json',
        dataType: 'json',                
    });
});