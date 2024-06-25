// YOUTUBE EMBED CODE ================================================
// YOUTUBE EMBED CODE ================================================
// YOUTUBE EMBED CODE ================================================

var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
var player;
function onYouTubeIframeAPIReady() {
player = new YT.Player('player', {
    height: '280',
    width: '498',
    events: {
    'onReady': onPlayerReady,
    'onStateChange': onPlayerStateChange
    }
});
}

// 4. The API will call this function when the video player is ready.
function onPlayerReady(event) {
    event.target.stopVideo();
}

// 5. The API calls this function when the player's state changes.
//    The function indicates that when playing a video (state=1),
//    the player should play for six seconds and then stop.
var done = false;
function onPlayerStateChange(event) {
if (event.data == YT.PlayerState.PLAYING && !done) {
    setTimeout(stopVideo, 6000);
    done = true;
}
}
function stopVideo() {
player.stopVideo();
}

// YOUTUBE EMBED CODE ================================================
// YOUTUBE EMBED CODE ================================================
// YOUTUBE EMBED CODE ================================================




// logic for the shift button (for quick deleting videos)
var shifted = false
$(document).on('keyup keydown', function(e){shifted = e.shiftKey} );

// search for the video with the given link
$(document).on('click', '.search input[type="submit"]', function (e) {
    var state = document.getElementById('video-id-search')

    var obj = {
        'url': state.value
    }
    var jsonObj = JSON.stringify(obj)

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/search",
        headers:{'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        data: jsonObj,
        cahce: true,
        success: function (result) {
            var response = JSON.parse(JSON.stringify(result))

            player.cueVideoById(response['id'])

            $("#kitchen-title").html(response['title'])
            $(".kitchen .info button").attr('data-id', response['id'])

            $('.video-formats').html('')
            $('.audio-formats').html('')
            $.each( response['videos'], function( index, value ) {
                $('.video-formats').append(`<option>${value}</option>`)
            });
            $.each( response['audios'], function( index, value ) {
              $('.audio-formats').append(`<option>${value}</option>`)
            });
        },
        contentType: 'application/json',
        dataType: 'json',                
    });
});




// adds video to the video list
function addPlate(response){
    if(document.getElementById(response['id']) == null)
    {
        var plate = $("#plate-template").html()
        plate = plate.replace('id="id"', `id="${response['id']}"`)
        
        $(".plates").prepend(plate)

        $(`.plates #${response['id']}`).attr('data-video-id', response['video_id'])
        $(`.plates #${response['id']} .plate-thumbnail img`).attr('src', response['thumbnail'])
        $(`.plates #${response['id']} .plate-title`).html(`<a href="https://youtu.be/${response['video_id']}">${response['title']}</a>`)
        $(`.plates #${response['id']} .plate-filename`).html(response['filename'])
        $(`.plates #${response['id']} .control-button`).attr('data-id', response['id'])
    }
}

// downloads video with the best quality
$(document).on('click', '.kitchen .info .download-best button', function (e) {

    var obj = {
        'id': $('.kitchen .info button').attr("data-id")
    }
    var jsonObj = JSON.stringify(obj)

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/download",
        headers:{'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        data: jsonObj,
        cahce: true,
        success: function (result) {
            var response = JSON.parse(JSON.stringify(result))

            addPlate(response)
        },
        contentType: 'application/json',
        dataType: 'json',                
    });
});
// downloads video with the choosen video and audio quality
$(document).on('click', '.kitchen .info .download-form button', function (e) {

    var obj = {
        'id': $('.kitchen .info button').attr("data-id"),
        'video': $('.video-combined option:selected').text(),
        'audio': $('.audio-combined option:selected').text(),
        'ext': $('.extension option:selected').text()
    }
    var jsonObj = JSON.stringify(obj)

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/download",
        headers:{'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        data: jsonObj,
        cahce: true,
        success: function (result) {
            var response = JSON.parse(JSON.stringify(result))

            addPlate(response)
        },
        contentType: 'application/json',
        dataType: 'json',                
    });
});
// downloads video with the choosen video quality
$(document).on('click', '.kitchen .info .download-video button', function (e) {

    var obj = {
        'id': $('.kitchen .info button').attr("data-id"),
        'video': $('.only-video-formats option:selected').text()
    }
    var jsonObj = JSON.stringify(obj)

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/download",
        headers:{'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        data: jsonObj,
        cahce: true,
        success: function (result) {
            var response = JSON.parse(JSON.stringify(result))

            addPlate(response)
        },
        contentType: 'application/json',
        dataType: 'json',                
    });
});
// downloads video with the choosen audio quality
$(document).on('click', '.kitchen .info .download-audio button', function (e) {

    var obj = {
        'id': $('.kitchen .info button').attr("data-id"),
        'audio': $('.only-audio-formats option:selected').text()
    }
    var jsonObj = JSON.stringify(obj)

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/download",
        headers:{'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        data: jsonObj,
        cahce: true,
        success: function (result) {
            var response = JSON.parse(JSON.stringify(result))

            addPlate(response)
        },
        contentType: 'application/json',
        dataType: 'json',                
    });
});
// downloads video with the choosen preset
$(document).on('click', '.kitchen .info .download-preset button', function (e) {

    var obj = {
        'id': $('.kitchen .info button').attr("data-id"),
        'preset': $('#choosen-preset').val(),
        'preset_name': $('.preset option:selected').first().html(),
    }
    var jsonObj = JSON.stringify(obj)

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/download",
        headers:{'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        data: jsonObj,
        cahce: true,
        success: function (result) {
            var response = JSON.parse(JSON.stringify(result))

            addPlate(response)
        },
        contentType: 'application/json',
        dataType: 'json',                
    });
});



// starts or pauses video downloading
$(document).on('click', '.start-stop', function (e) {

    var obj = {
        'id': e.currentTarget.dataset.id
    }
    var jsonObj = JSON.stringify(obj)

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/startstop",
        headers:{'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        data: jsonObj,
        cahce: true,
        success: function (result) {

        },
        contentType: 'application/json',
        dataType: 'json',                
    });
});
// deletes video from the list
$(document).on('click', '.delete', function (e) {

    var obj = {
        'id': e.currentTarget.dataset.id
    }
    var jsonObj = JSON.stringify(obj)

    if (!shifted){
        if (!window.confirm("Do you really want to delete this entry?\nThe file will remain, you have to delete it manually if necessary")) {
            return false
        }
    }

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/delete",
        headers:{'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        data: jsonObj,
        cahce: true,
        success: function (result) {
            var response = JSON.parse(JSON.stringify(result))
            
            if (response['status'] == 'deleted'){
                $("#" + response["id"]).remove()
            }

        },
        contentType: 'application/json',
        dataType: 'json',                
    });
});



// video download progress =================================
// video download progress =================================
var progress_update = window.setInterval(getDownloadInfo, 1000);

function startUpdating(){
    progress_update = window.setInterval(getDownloadInfo, 1000);
}
function stopUpdating(){ 
    clearInterval(progress_update)
}

// window.addEventListener("focus", startUpdating)
// window.addEventListener("blur", stopUpdating)

function format_bytes(bytes, speed = false){

    const names = {
        0: 'B',
        1: 'KB',
        2: 'MB',
        3: 'GB',
        4: 'TB'
    }

    var last_reduced = bytes
    var reduced = bytes

    for (let i = 1; i < 5; i++){

        last_reduced = reduced
        reduced /= 1000

        if (reduced < 0.9){
            return `${last_reduced.toFixed(2)} ${names[i-1]}${speed ? '/s' : ''}`
        }

    }
    return `${last_reduced.toFixed(2)} ${names[4]}${speed ? '/s' : ''}`

}

function formatETA(seconds){
    if (seconds > 60){
        return `${Math.floor(seconds/60)}m${String(seconds%60).padStart(2, '0')}s`
    }
    return `${seconds}s`
}

function getDownloadInfo(){
    
    var ids = []
    $(".plate").each(function( index ) {
        ids.push($(this).attr('id'))
    });

    var obj = {
        'ids': ids
    }
    var jsonObj = JSON.stringify(obj)
    
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/checkplate",
        headers:{'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        data: jsonObj,
        cahce: true,
        success: function (result) {
            var response = JSON.parse(JSON.stringify(result))

            jQuery.each(response, function(i, val) {
                if (val["done"] == true){
                    $("#" + i + " .plate-speed").html('<b><i class="material-symbols-outlined status-icon">done_outline</i> <i>Done</i></b>');
                }
                else if (val["speed"] == "Paused"){
                    $("#" + i + " .plate-speed").html(`<i><b><i class="material-symbols-outlined status-icon">pause</i> Paused</b></i>`);
                }
                else{
                    $("#" + i + " .plate-speed").html(`${format_bytes(val["speed"], true)} (ETA: ${formatETA(val['eta'])})`);
                }
                
                $("#" + i + " .plate-options").html(val['options'])
                $("#" + i + " .plate-error").html(val['error'])

                $("#" + i + " progress").attr('value', val["total"] > 0 ?  (val["downloaded"] / val["total"] * 100).toFixed(2) : 100);
                $("#" + i + " .plate-percents").html(`<i>${val["total"] > 0 ? (val["downloaded"] / val["total"] * 100).toFixed(2) : '?'}%</i>`);
                $("#" + i + " .plate-downloaded").html(`<i>${format_bytes(val["downloaded"])} / ${val["total"] > 0 ? format_bytes(val["total"]) : '? bytes'}</i>`);
              });
        },
        contentType: 'application/json',
        dataType: 'json',                
    });
}
// video download progress =================================
// video download progress =================================



// choose first preset on the page load
$(document).ready(function() { 
    var preset_value = $('.preset-values').first().attr('data-preset')
    $('#choosen-preset').attr('value', preset_value)
});

// set preset data into field on preset choose
$(document).on( "change", ".preset", function() {
    var name = $('.preset option:selected').first().html()
    $('#choosen-preset').val($(`.preset-values[data-name="${name}"]`).first().attr('data-preset'))
});
