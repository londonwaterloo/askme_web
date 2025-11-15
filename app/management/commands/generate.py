from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import (
    Profile,
    Tag,
    Question,
    Answer,
    LikeQ,
    LikeA
)
import random


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)
        parser.add_argument('offset', type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']
        offset = options['offset']

        self.profiles_gen(ratio, offset)
        profiles = list(Profile.objects.all())

        self.tags_gen(ratio, offset)
        tags = list(Tag.objects.all())

        self.questions_gen(profiles, ratio, offset)
        questions = list(Question.objects.all())

        self.answers_gen(profiles, questions, ratio, offset)
        answers = list(Answer.objects.all())

        self.q_likes_gen(profiles, questions, ratio)

        self.a_likes_gen(profiles, answers, ratio)

        for question in questions:
            question.tags.add(*random.sample(tags, k=3))

        self.stdout.write(self.style.SUCCESS("Database successfully filled!"))



    def profiles_gen(self, ratio, offset):
        self.stdout.write("Generating profiles...")

        profiles = []

        for i in range(ratio):
            if i % 1000 == 0:
                print(f'{i} profiles generated')

            username = f'user_{i + offset}'

            user = User.objects.create_user(
                username=username,
                first_name=f'Bot{i}',
                last_name=f'AFK{i}',
                email=f'{username}@mail.com',
                password="q1w2e3r4",
                is_active=True
            )

            profiles.append(Profile(user=user))

        Profile.objects.bulk_create(profiles)



    def tags_gen(self, count, offset):
        self.stdout.write("Generating tags...")

        tags = []

        for i in range(count):
            if i % 1000 == 0:
                print(f'{i} tags generated')

            tags.append(Tag(title=f'tag_{i + offset}'))

        Tag.objects.bulk_create(tags)



    def questions_gen(self, profiles, ratio, offset):
        self.stdout.write("Generating questions...")

        questions = []

        for i in range(10 * ratio):
            if i % 5000 == 0:
                print(f'{i} questions generated')

            questions.append(
                Question(
                    author=random.choice(profiles),
                    title=f'Question {i + offset}',
                    text="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
                )
            )

        Question.objects.bulk_create(questions)



    def answers_gen(self, profiles, questions, ratio, offset):
        self.stdout.write("Generating answers...")

        answers = []

        for i in range(100 * ratio):
            if i % 50000 == 0:
                print(f'{i} answers generated')

            answers.append(
                Answer(
                    author=random.choice(profiles),
                    question=random.choice(questions),
                    text=f'Answer text {i + offset}'
                )
            )

            # flush cache for large batches
            if len(answers) >= 500000:
                Answer.objects.bulk_create(answers)
                answers = []

        if answers:
            Answer.objects.bulk_create(answers)



    def q_likes_gen(self, profiles, questions, ratio):
        self.stdout.write("Generating question likes...")

        used_pairs = set()
        likes = []

        total = 150 * ratio

        for i in range(total):
            if i % 50000 == 0:
                print(f'{i} question likes generated')

            # generate unique pair (user, question)
            while True:
                user = random.choice(profiles)
                question = random.choice(questions)
                pair = (user.id, question.id)

                if pair not in used_pairs:
                    used_pairs.add(pair)
                    break

            likes.append(
                LikeQ(
                    user=user,
                    question=question,
                    value=random.choice([1, -1])
                )
            )

            if len(likes) >= 300000:
                LikeQ.objects.bulk_create(likes)
                likes = []

        if likes:
            LikeQ.objects.bulk_create(likes)



    def a_likes_gen(self, profiles, answers, ratio):
        self.stdout.write("Generating answer likes...")

        used_pairs = set()
        likes = []

        total = 50 * ratio

        for i in range(total):
            if i % 20000 == 0:
                print(f'{i} answer likes generated')

            while True:
                user = random.choice(profiles)
                answer = random.choice(answers)

                pair = (user.id, answer.id)

                if pair not in used_pairs:
                    used_pairs.add(pair)
                    break

            likes.append(
                LikeA(
                    user=user,
                    answer=answer,
                    value=random.choice([1, -1])
                )
            )

            if len(likes) >= 300000:
                LikeA.objects.bulk_create(likes)
                likes = []

        if likes:
            LikeA.objects.bulk_create(likes)
