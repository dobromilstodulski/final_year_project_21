//var socket;
$(document).ready(function () {
    //socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    var socket = io.connect('http://127.0.0.1:5000');


    socket.on('connect', function () {
        socket.send('User has joined the chat!');
    });

    socket.on('message', function (msg) {
        $('#messages').append('<li>'+msg+'</li>');
        console.log('Received message');
    });

    $(sendmessage).on('click', function () {
        socket.send($('#myMessage').val());
        $('#myMessage').val('');
    });
});