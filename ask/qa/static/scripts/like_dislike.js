'use strict'

function like(url) {
    $.ajax({
        data: {},
        type: 'post',
        url: url,
        headers: { 'X-CSRFToken': csrftoken },
        success: function (data) {
            $(`#rating_${ data.id }`).html(data.rating);
            let like_button = $(`#like_${ data.id }`);
            let dislike_button = $(`#dislike_${ data.id }`);
            like_button.removeClass('active');
            dislike_button.removeClass('active');
            if ( data.result ) {
                $(`#like_${ data.id }`).addClass('active');
            }
        },
        error: function (data) { console.log(data.responseJSON.error); },
    });
}

function dislike(url) {
    $.ajax({
        data: {},
        type: 'post',
        url: url,
        headers: { 'X-CSRFToken': csrftoken },
        success: function (data) {
            $(`#rating_${ data.id }`).html(data.rating);
            let like_button = $(`#like_${ data.id }`);
            let dislike_button = $(`#dislike_${ data.id }`);
            like_button.removeClass('active');
            dislike_button.removeClass('active');
            if ( data.result ) {
                $(`#dislike_${ data.id }`).addClass('active');
            }
        },
        error: function (data) { console.log(data.responseJSON.error); },
    });
}

function is_like(num) {
    if ( num == 1 ) { return 'active' }
}

function is_dislike(num) {
    if ( num == -1 ) { return 'active' }
}
