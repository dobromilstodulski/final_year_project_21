document.getElementById("playPauseAudio{{song.id}}").onclick = function() {
    var audio = document.getElementById("audio{{song.id}}");
    if (audio.paused) audio.play();
    else audio.pause();
};