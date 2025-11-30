from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
import datetime


# -------------------------
# Managers
# -------------------------

class QuestionManager(models.Manager):
    def get_hot_questions(self):
        # сортировка по количеству лайков
        return self.annotate(
            likes_count=Count('likes')
        ).order_by('-likes_count', '-date')

    def get_recent_questions(self):
        return self.order_by('-date')

    def get_questions_for_tag(self, title):
        return self.filter(tags__title=title)

    def get_questions_for_user(self, user_id):
        return self.filter(author__user_id=user_id)


class AnswerManager(models.Manager):
    def get_answers_for_question(self, q_id):
        return self.filter(question_id=q_id)


class TagManager(models.Manager):
    def get_tag_by_title(self, title):
        return self.get(title=title)

    def get_hot_tags(self):
        return self.annotate(count=Count('questions')).order_by('-count')[:9]


class ProfileManager(models.Manager):
    def get_top_users(self):
        return self.annotate(
            rating=0.3 * Count('answer') + 0.1 * Count('question')
        ).order_by('-rating')[:10]


class LikeQManager(models.Manager):
    def get_likes_count_for_question(self, q_id):
        return self.filter(question_id=q_id).count()


class LikeAManager(models.Manager):
    def get_likes_count_for_answer(self, a_id):
        return self.filter(answer_id=a_id).count()


# -------------------------
# Models
# -------------------------

class Profile(models.Model):
    objects = ProfileManager()

    user = models.OneToOneField(User, null=True, related_name='profile', on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to='profiles/avatars/')
    bio = models.TextField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    objects = TagManager()

    title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    objects = QuestionManager()

    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True, related_name='questions')
    date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=5000)

    def get_like_count(self):
        return self.likes.count()

    def get_answer_count(self):
        return self.answers.count()

    def __str__(self):
        return self.title


class Answer(models.Model):
    objects = AnswerManager()

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    text = models.TextField()
    solution = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.title}_answer"


class LikeQ(models.Model):
    objects = LikeQManager()

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes')

    value = models.IntegerField(
        choices=[(1, 'Like'), (-1, 'Dislike')],
        default=1
    )

    class Meta:
        unique_together = ('user', 'question')


class LikeA(models.Model):
    objects = LikeAManager()

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')

    value = models.IntegerField(
        choices=[(1, 'Like'), (-1, 'Dislike')],
        default=1
    )

    class Meta:
        unique_together = ('user', 'answer')
