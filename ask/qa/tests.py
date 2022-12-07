from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from .models import Question, LikeDislike


def create_test_user():
    return User.objects.create_user(
        username='username',
        password='password',
    )


class QuestionModelTests(TestCase):
    def test_short_text_with_long_text(self):
        """
        Длинный текст должен обрезаться до 203 символов.
        """
        title = 'test'
        text = 'test' * 100
        question = Question.objects.create(title=title, text=text, author=create_test_user())
        self.assertEqual(len(question.text_short), 203)

    def test_short_text_with_short_text(self):
        """
        Короткий текст не должен изменяться.
        """
        title = 'test'
        text = 'test'
        question = Question.objects.create(title=title, text=text, author=create_test_user())
        self.assertEqual(question.text_short, text)


class LikeDislikeManagerTests(TestCase):
    def test_is_like_dislike_with_like(self):
        """
        Если пользователь поставил лайк, функция должна вернуть 1.
        """
        user = create_test_user()
        question = Question.objects.create(title='title', text='text', author=user)
        question.votes.create(user=user, vote=LikeDislike.LIKE)
        self.assertEqual(question.votes.is_like_dislike(user, question), 1)

    def test_is_like_dislike_with_dislike(self):
        """
        Если пользователь поставил лайк, функция должна вернуть -1.
        """
        user = create_test_user()
        question = Question.objects.create(title='title', text='text', author=user)
        question.votes.create(user=user, vote=LikeDislike.DISLIKE)
        self.assertEqual(question.votes.is_like_dislike(user, question), -1)

    def test_is_like_dislike_with_no_reaction(self):
        """
        Если пользователь не реагировал на запись, функция должна вернуть 0.
        """
        user = create_test_user()
        question = Question.objects.create(title='title', text='text', author=user)
        self.assertEqual(question.votes.is_like_dislike(user, question), 0)

    def test_set_like_or_dislike_or_remove_with_set_like_first(self):
        """
        Пользователь поставил лайк первый раз.
        """
        vote_type = LikeDislike.LIKE
        user = create_test_user()
        question = Question.objects.create(title='title', text='text', author=user)
        self.assertIs(question.votes.set_like_or_dislike_or_remove(question, user, vote_type), True)
        self.assertEqual(question.votes.is_like_dislike(user, question), 1)

    def test_set_like_or_dislike_or_remove_with_set_dislike_first(self):
        """
        Пользователь поставил дизлайк первый раз.
        """
        vote_type = LikeDislike.DISLIKE
        user = create_test_user()
        question = Question.objects.create(title='title', text='text', author=user)
        self.assertIs(question.votes.set_like_or_dislike_or_remove(question, user, vote_type), True)
        self.assertEqual(question.votes.is_like_dislike(user, question), -1)

    def test_set_like_or_dislike_or_remove_with_unset_like(self):
        """
        Пользователь убрал лайк.
        """
        vote_type = LikeDislike.LIKE
        user = create_test_user()
        question = Question.objects.create(title='title', text='text', author=user)
        question.votes.create(user=user, vote=vote_type)
        self.assertIs(question.votes.set_like_or_dislike_or_remove(question, user, vote_type), False)
        self.assertEqual(question.votes.is_like_dislike(user, question), 0)

    def test_set_like_or_dislike_or_remove_with_unset_dislike(self):
        """
        Пользователь убрал дизлайк.
        """
        vote_type = LikeDislike.DISLIKE
        user = create_test_user()
        question = Question.objects.create(title='title', text='text', author=user)
        question.votes.create(user=user, vote=vote_type)
        self.assertIs(question.votes.set_like_or_dislike_or_remove(question, user, vote_type), False)
        self.assertEqual(question.votes.is_like_dislike(user, question), 0)

    def test_set_like_or_dislike_or_remove_with_set_like_with_active_dislike(self):
        """
        Пользователь поставил лайк с активным дизлайком.
        """
        user = create_test_user()
        question = Question.objects.create(title='title', text='text', author=user)
        question.votes.create(user=user, vote=LikeDislike.DISLIKE)
        self.assertIs(question.votes.set_like_or_dislike_or_remove(question, user, LikeDislike.LIKE), True)
        self.assertEqual(question.votes.is_like_dislike(user, question), 1)

    def test_set_like_or_dislike_or_remove_with_set_dislike_with_active_like(self):
        """
        Пользователь поставил дизлайк с активным лайком.
        """
        user = create_test_user()
        question = Question.objects.create(title='title', text='text', author=user)
        question.votes.create(user=user, vote=LikeDislike.LIKE)
        self.assertIs(question.votes.set_like_or_dislike_or_remove(question, user, LikeDislike.DISLIKE), True)
        self.assertEqual(question.votes.is_like_dislike(user, question), -1)
