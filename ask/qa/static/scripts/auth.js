'use strict'

$(document).ready(function() {
    $('.needs-validation').attr('novalidate', 'novalidate');
    $('.needs-validation').submit(function (event) {
        if ( validation() ) {
            $.ajax({
                data: $(this).serialize(),
                type: $(this).attr('method'),
                url: location.href,
                success: function (data) {
                    window.location = data.url;
                },
                error: function (data) {
                    addFormErrors(data.responseJSON.error);
                },
            });
        }
        return false;
    });
});

function validation() {
    let val = true;
    $('.needs-validation .form-control').each(function () {
        if ( !$(this).val() ) {
            val = false;
            $(this).addClass('is-invalid');
            $(this).next().html('Данное поле не может быть пустым');
        }
        focusRemoveClass($(this));
    })
    return val;
}

function addFormErrors(formErrors) {
    for (let inputId in formErrors) {
        let form = $(`#${ inputId }`);
        form.addClass('is-invalid');
        form.next().html(formErrors[inputId].filter(error => error).join('<br>'));
    }
}

function focusRemoveClass(form) {
    form.focus(function () {
        form.removeClass('is-invalid');
        form.next().html('');
    })
}