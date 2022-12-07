from django.utils.formats import localize
from django.utils.timezone import template_localtime
from django.utils.html import escape
from django.urls import reverse


def serialize_new_answer(answer, user):
    return {
        'id': answer.id,
        'text': escape(answer.text),
        'added_at': localize(template_localtime(answer.added_at)),
        'author': escape(user.username),
        'question_id': answer.question_id,
        'url_delete': reverse('qa:delete_answer'),
        'is_user': True,
        'is_like_dislike': 0,
        'url_like': reverse('qa:like_answer', args=[answer.id]),
        'url_dislike': reverse('qa:dislike_answer', args=[answer.id]),
        'rating': 0,
    }


def serialize_answers(page_obj, user):
    answers = {}
    number = 0
    for answer in page_obj:
        is_user = user.username == answer.author.username
        answers[number] = {
            'id': answer.id,
            'text': escape(answer.text),
            'author': escape(answer.author.username),
            'question_id': answer.question_id,
            'added_at': localize(template_localtime(answer.added_at)),
            'url_like': reverse('qa:like_answer', args=[answer.id]),
            'url_dislike': reverse('qa:dislike_answer', args=[answer.id]),
            'rating': answer.votes.rating(),
        }
        if user.is_authenticated:
            answers[number]['is_like_dislike'] = answer.votes.is_like_dislike(user, answer)
            if is_user:
                answers[number]['url_delete'] = reverse('qa:delete_answer')
                answers[number]['is_user'] = is_user
        number += 1
    return {'has_page': page_obj.has_next(), 'answers': answers}


def serialize_questions(page_obj, user):
    questions = {}
    number = 0
    for question in page_obj:
        is_user = user.username == question.author.username
        questions[number] = {
            'id': question.id,
            'title': escape(question.title),
            'text_short': escape(question.text_short),
            'author': escape(question.author.username),
            'url_detail': reverse('qa:question', args=[question.id]),
            'url_like': reverse('qa:like_question', args=[question.id]),
            'url_dislike': reverse('qa:dislike_question', args=[question.id]),
            'answers_count': question.answer_set.count(),
            'rating': question.votes.rating(),
        }
        if user.is_authenticated:
            questions[number]['is_like_dislike'] = question.votes.is_like_dislike(user, question)
            if is_user:
                questions[number]['url_delete'] = reverse('qa:delete_question')
                questions[number]['is_user'] = is_user
        number += 1
    page = {
        'number': page_obj.number,
        'num_pages': page_obj.paginator.num_pages,
        'previous_active': page_obj.has_previous(),
        'next_active': page_obj.has_next(),
        'count': page_obj.paginator.count,
    }
    return {'page': page, 'questions': questions}
