'use strict'

$(document).ready(function() {
    loadQuestions(1, 'new');
});

function changeOption(sort_option) {
    $('#sortOption button').removeClass('active');
    $(`#${sort_option}`).addClass('active');
    loadQuestions(1, sort_option);
}

function loadQuestions(page, sort_option) {
    $.ajax({
        data: {
            'page': page,
            'sort_option': sort_option,
        },
        type: 'get',
        url: location.href,
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        success: function (data) {
            let questions = data.questions;
            let questionsHtml = '';
            for (let num in questions) {
                questionsHtml += createQuestion(questions[num]);
            }
            $('#questions').html(questionsHtml);
            let paginator = new Paginator(data, sort_option);
            let paginatorHtml = paginator.createPaginator();
            $('#paginator').html(paginatorHtml);
            $('#searchCount').html(data.page.count);
        },
        error: function (data) { console.log(data.responseJSON.error); },
    });
}

function createQuestion(data) {
    let delete_button = '';
    let questionHtml = `<div class="card my-3" id="${ data.id }">
                            <div class="card-body">
                                <div class="d-flex justify-content-between">
                                    <div class="d-flex">
                                    <a class="text-decoration-none" href="${ data.url_detail }" ><h5 class="card-title d-flex">${ data.title }</h5></a>
                                    <h6 class="card-subtitle mt-1 mx-3 text-muted">${ data.author }</h6>
                                    </div>
                                    ${ delete_button }
                                </div>
                                <p class="card-text">${ data.text_short }</p>
                            </div>
                            <div class="d-flex justify-content-between px-3">
                                <p class="card-text">Ответов: ${ data.answers_count }</p>
                                <div class="d-flex">
                                    <h5 id="rating_${ data.id }" class="mx-2">${ data.rating }</h5>
                                    <button id="like_${ data.id }" class="like mx-2 ${is_like(data.is_like_dislike)}" onclick="like('${ data.url_like }')"></button>
                                    <button id="dislike_${ data.id }" class="dislike ${is_dislike(data.is_like_dislike)}" onclick="dislike('${ data.url_dislike }')"></button>
                                </div>
                            </div>
                        </div>`;
    return questionHtml;
}

class Paginator {
    first = 'Первая';
    previous = '&laquo;';
    next = '&raquo;';
    last = 'Последняя';

    constructor(data, sort_option) {
        this.sort_option = sort_option;
        this.page = data.page.number;
        this.numPages = data.page.num_pages;
        this.previousActive = data.page.previous_active;
        this.nextActive = data.page.next_active;
    }

    createPaginator() {
        return this._createPreviousBlock() + this._createMiddleBlock() + this._createNextBlock();
    }

    _createPreviousBlock(active) {
        return this._createBlock(this.first, this.previousActive, 1) + this._createBlock(this.previous, this.previousActive, this.page-1);
    }

    _createMiddleBlock() {
        let middleBlock = '';
        for (let i = Math.max(this.page-3, 1); i < this.page; i++) {
            middleBlock += this._createBlock(i, true, i);
        }
        middleBlock += this._createBlock(this.page, 'active', this.page);
        for (let i = this.page+1; i < Math.min(this.page+4, this.numPages+1); i++) {
            middleBlock += this._createBlock(i, true, i);
        }
        return middleBlock;
    }

    _createNextBlock(active) {
        return this._createBlock(this.next, this.nextActive, this.page+1) + this._createBlock(this.last, this.nextActive, this.numPages);
    }

    _createBlock(value, active, num) {
        return `<li class="page-item ${ this.is_active(active) }">
                    <button class="page-link" onclick="loadQuestions(${ num }, '${ this.sort_option }')">
                        <span aria-hidden="true">${ value }</span>
                    </button>
                </li>`;
    }

    is_active(active) {
        if ( !active ) { return 'disabled'; }
        else if ( active == 'active' ) { return 'active' }
        else { return ''; }
    }
}
