'use strict'

const csrftoken = getCookie('csrftoken');

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

function createAnswer(data) {
    let answerHtml = `<div class="card my-3" id="${ data.answer_id }">
                          <div class="card-body">
                              <div class="d-flex justify-content-between">
                                  <h5 class="card-title">${ data.author }</h5>
                                  <form method="post">
                                      <button type="button" class="btn-close d-flex" onclick="AjaxRemoveAnswer('${ data.url_delete }',${ data.question_id }, ${ data.answer_id })" aria-label="Delete"></button>
                                  </form>
                              </div>
                              <p class="card-text">${ data.text }</p>
                              <time class="text-muted"><small>${ data.added_at }</small></time>
                          </div>
                      </div>`;
    return answerHtml
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
        success: function (data) {
                let elem = document.getElementById(AnswerRemoveId);
                elem.parentNode.removeChild(elem);
            },
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
