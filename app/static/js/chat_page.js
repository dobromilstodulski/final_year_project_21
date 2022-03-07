var socket;
$(document).ready(function () {
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');

    socket.on('connect', function () {
        socket.send('User has joined the chat!');
    });

    socket.on('message', function (msg) {
        $('#messages').append($('<li>').text(msg));
        console.log('Received message');
    });

    $(sendmessage).on('click', function () {
        socket.send($('#message').val());
        $('#message').val('');
    });
});