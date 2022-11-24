'use strict'

const csrftoken = getCookie('csrftoken');

let hasPage = true;
let page = 1;

$(document).ready(function() {
    loadOnScroll();
});

$(document).ready(function() {
    $('#answer_form').submit(function () {
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: location.href,
            success: function (data) {
                $('#answer_form')[0].reset();
                let answerHtml = createAnswer(data)
                $('#answers').prepend(answerHtml);
            },
            error: function (data) { console.log(data.responseJSON.error) },
        });
        return false;
    })
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function AjaxRemoveAnswer(url, QuestionRemoveId, AnswerRemoveId) {
    $.ajax({
        data: {
            question_id: QuestionRemoveId,
            answer_id: AnswerRemoveId,
        },
        type: 'post',
        url: url,
        headers: {'X-CSRFToken': csrftoken},
        success: function (data) { document.getElementById(AnswerRemoveId).remove(); },
        error: function() { console.log(data.responseJSON.error); },
    })
}

function AjaxRemoveQuestion(url, removeId, urlRedirect) {
    $.ajax({
        data: {
            id: removeId,
        },
        type: 'post',
        url: url,
        headers: {'X-CSRFToken': csrftoken},
        success: function (data) { window.location = urlRedirect; },
        error: function() { console.log(data.responseJSON.error); },
    })
}

function loadOnScroll() {
    if ($(window).scrollTop() > $(document).height() - $(window).height() * 2) {
        $(window).unbind();
        loadItems();
    }
}

function loadItems() {
    $.ajax({
        data: {'page': page },
        type: 'get',
        url: location.href + '/load_answers',
        success: function(data) {
            hasPage = data.has_page;
            let answers = data.answers;
            for (let num in answers) {
                let answerHtml = createAnswer(answers[num]);
                $('#answers').append(answerHtml);
            }
            if (hasPage) {
                page++;
                $(window).bind('scroll', loadOnScroll);
            }
        },
        error: function() { console.log(data.responseJSON.error); },
    });
}

function createAnswer(data) {
    let delete_button = CreateDeleteButton(data);
    let answerHtml = `<div class="card my-3" id="${ data.answer_id }">
                          <div class="card-body">
                              <div class="d-flex justify-content-between">
                                  <h5 class="card-title">${ data.author }</h5>
                                  ${ delete_button }
                              </div>
                              <p class="card-text">${ data.text }</p>
                              <time class="text-muted"><small>${ data.added_at }</small></time>
                          </div>
                      </div>`;
    return answerHtml
}

function CreateDeleteButton(data) {
    if (data.is_user) {
        return `<form method="post">
                    <button type="button" class="btn-close d-flex" onclick="AjaxRemoveAnswer('${ data.url_delete }',${ data.question_id }, ${ data.answer_id })" aria-label="Delete"></button>
                </form>`
    } else { return '' }
}