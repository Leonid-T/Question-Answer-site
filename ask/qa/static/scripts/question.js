'use strict'

let hasPage = true;
let page = 1;

$(document).ready(function() {
    loadOnScroll('new');
});

$(document).ready(function() {
    $('#answer_form').submit(function () {
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: location.href,
            success: function (data) {
                $('#answer_form')[0].reset();
                let answerHtml = createAnswer(data);
                $('#answers').prepend(answerHtml);
            },
            error: function (data) { console.log(data.responseJSON.error); },
        });
        return false;
    })
});

function AjaxRemoveAnswer(url, QuestionRemoveId, AnswerRemoveId) {
    $.ajax({
        data: {
            question_id: QuestionRemoveId,
            answer_id: AnswerRemoveId,
        },
        type: 'post',
        url: url,
        headers: { 'X-CSRFToken': csrftoken },
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
        headers: { 'X-CSRFToken': csrftoken },
        success: function (data) { window.location = urlRedirect; },
        error: function() { console.log(data.responseJSON.error); },
    })
}

function loadOnScroll(sort_option) {
    if ($(window).scrollTop() > $(document).height() - $(window).height() * 2) {
        $(window).unbind();
        loadItems(sort_option);
    }
}

function loadItems(sort_option) {
    $.ajax({
        data: {
            'sort_option': sort_option,
            'page': page,
        },
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
                $(window).bind('scroll', function () { loadOnScroll(sort_option) });
            }
        },
        error: function() { console.log(data.responseJSON.error); },
    });
}

function createAnswer(data) {
    let delete_button = CreateDeleteButton(data);
    let answerHtml = `<div class="card my-3" id="${ data.id }">
                          <div class="card-body">
                              <div class="d-flex justify-content-between">
                                  <h5 class="card-title">${ data.author }</h5>
                                  ${ delete_button }
                              </div>
                              <p class="card-text">${ data.text }</p>
                          </div>
                          <div class="d-flex justify-content-between px-3">
                              <time class="text-muted"><small>${ data.added_at }</small></time>
                              <div class="d-flex">
                                  <h5 id="rating_${ data.id }" class="mx-2">${ data.rating }</h5>
                                  <button id="like_${ data.id }" class="like mx-2 ${is_like(data.is_like_dislike)}" onclick="like('${ data.url_like }')"></button>
                                  <button id="dislike_${ data.id }" class="dislike ${is_dislike(data.is_like_dislike)}" onclick="dislike('${ data.url_dislike }')"></button>
                              </div>
                          </div>
                      </div>`;
    return answerHtml;
}

function CreateDeleteButton(data) {
    if (data.is_user) {
        return `<form method="post">
                    <button type="button" class="btn-close d-flex" onclick="AjaxRemoveAnswer('${ data.url_delete }',${ data.question_id }, ${ data.id })" aria-label="Delete"></button>
                </form>`
    } else { return '' }
}

function changeOption(sort_option) {
    $('#sortOption button').removeClass('active');
    $(`#${sort_option}`).addClass('active');
    $('#answers').html('');
    page = 1;
    loadOnScroll(sort_option);
}