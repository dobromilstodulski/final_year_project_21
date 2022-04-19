var socket;
$(document).ready(function () {
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socket.on('connect', function () {
        socket.emit('joined', {});
    });
    socket.on('status', function (data) {
        $("#messages").append('<li>' + data.msg + '</li>');
        console.log('Received message');
    });
    socket.on('message', function (data) {
        $("#messages").append('<li>' + data.msg + '</li>');
        console.log('Received message');
    });
    $('#sendmessage').on('click', function() {
        text = $('#myMessage').val();
        $('#myMessage').val('');
        socket.emit('text', {msg: text});
	})
});
function leave_room() {
    socket.emit('left', {}, function () {
        socket.disconnect();

        // go back to the login page
        window.location.href = "{{ url_for('main.index') }}";
    });
}