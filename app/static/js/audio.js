$(document).ready(function () {
    document.getElementById("playPauseAudio{{song.id}}").onclick = function () {
        var audio = document.getElementById("audio{{song.id}}");
        var id = $(this).attr("song_id");
        if (audio.paused) {
            audio.play();

            req = $.ajax({
                url: '/stream/' + id,
                type: 'POST',
                dataType: 'html',
            });

            req.done(function (data) {
                console.log(data);
            });
        }
        else { audio.pause() };
    };
});