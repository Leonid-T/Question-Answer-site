from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def is_like_dislike(self, user, obj_id):
        try:
            return self.get(user=user, object_id=obj_id).vote
        except (KeyError, LikeDislike.DoesNotExist):
            return 0

    def rating(self):
        return self.aggregate(models.Sum('vote')).get('vote__sum') or 0

    def get_or_create_or_remove(self, obj, user, vote_type):
        try:
            like_dislike = LikeDislike.objects.get(
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.id,
                user=user
            )
            if like_dislike.vote is not vote_type:
                like_dislike.vote = vote_type
                like_dislike.save(update_fields=['vote'])
                return True
            else:
                like_dislike.delete()
                return False
        except (KeyError, LikeDislike.DoesNotExist):
            obj.votes.create(user=user, vote=vote_type)
            return True


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (LIKE, 'Нравится'),
        (DISLIKE, 'Не нравится'),
    )

    vote = models.SmallIntegerField(choices=VOTES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-added_at')

    def popular(self):
        return self.all()


class Question(models.Model):
    objects = QuestionManager()
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(blank=True, auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='question_like_user')
    votes = GenericRelation(LikeDislike, related_query_name='questions')

    def __str__(self):
        return self.title

    @property
    def answers(self):
        return self.answer_set.order_by('-added_at')

    @property
    def text_short(self):
        size = 200
        if len(self.text) > size:
            return f'{self.text[:size]}...'
        else:
            return self.text


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateTimeField(blank=True, auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    votes = GenericRelation(LikeDislike, related_query_name='answers')

    def __str__(self):
        return self.text
