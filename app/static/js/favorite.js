$(document).ready(function () {
    $(document).on('click', '.favorite', function (event) {

        event.preventDefault();

        var id = $(this).data("id");

        req = $.ajax({
            url: '/favorite/' + id,
            type: 'POST',
            dataType: 'html',
        });

        req.done(function (data) {
            console.log(data);
            $('#songReactions' + id).fadeOut(0).fadeIn(0);
            $('#songReactions' + id).html(data);
        });
    });

    $(document).on('click', '.unfavorite', function (event) {

        event.preventDefault();

        var id = $(this).data("id");

        req = $.ajax({
            url: '/unfavorite/' + id,
            type: 'POST',
            dataType: 'html',
        });

        req.done(function (data) {
            console.log(data);
            $('#songReactions' + id).fadeOut(0).fadeIn(0);
            $('#songReactions' + id).html(data);
        });
    });
});