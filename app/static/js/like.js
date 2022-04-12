$(document).ready(function () {
    $(document).on('click', '.like', function (event) {

        event.preventDefault();

        var id = $(this).data("id");

        req = $.ajax({
            url: '/like/' + id,
            type: 'POST',
            dataType: 'html',
        });

        req.done(function (data) {
            console.log(data);
            $('#postReactions' + id).fadeOut(0).fadeIn(0);
            $('#postReactions' + id).html(data);
        });
    });

    $(document).on('click', '.unlike', function (event) {

        event.preventDefault();

        var id = $(this).data("id");

        req = $.ajax({
            url: '/unlike/' + id,
            type: 'POST',
            dataType: 'html',
        });

        req.done(function (data) {
            console.log(data);
            $('#postReactions' + id).fadeOut(0).fadeIn(0);
            $('#postReactions' + id).html(data);
        });
    });
});