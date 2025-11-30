from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.contrib import messages

from app import models
from app.models import Question, Answer, Tag, Profile

top_users = models.Profile.objects.get_top_users()[:10]
top_tags = models.Tag.objects.get_hot_tags()[:10]


def create_content_right():
    content = {
        "tags": top_tags,
        "users": top_users,
    }

    return content


def create_content(objects, request):
    """Функция осуществляет пагинацию
    переданных объектов и
    добавляет контент для боковой панели"""
    page = pagination(objects, request)
    content = create_content_right()
    content["content"] = page
    return content


PER_PAGE = 10


def pagination(objects, request):
    paginator = Paginator(objects, PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page


def index(request):
    context = create_content(models.Question.objects.get_recent_questions(), request)
    return render(request, 'index.html', context)


def hot(request):
    context = create_content(models.Question.objects.get_hot_questions(), request)
    return render(request, 'hot.html', context)


def ask(request):
    context = create_content_right()
    return render(request, 'question_form.html', context)


def question_page(request, q_id):
    question = models.Question.objects.prefetch_related('tags').get(id=q_id)

    if request.method == "POST":
        # Проверяем, авторизован ли пользователь
        if request.user.is_authenticated:
            # Получаем текст ответа из формы
            answer_text = request.POST.get('answer_text')

            if answer_text:
                # Создаем новый ответ
                new_answer = models.Answer(
                    question=question,
                    author=request.user.profile,  # используем профиль пользователя
                    text=answer_text
                )
                new_answer.save()  # Сохраняем ответ в базе данных

                # После добавления ответа, перенаправляем на текущую страницу с новым ответом
                return redirect('question', q_id=q_id)
        else:
            # Если пользователь не авторизован, редиректим на страницу входа
            return redirect('login')

    # Получаем существующие ответы
    context = create_content(models.Answer.objects.get_answers_for_question(q_id), request)
    context["question"] = question

    return render(request, 'question_page.html', context)


def registration(request):
    context = create_content_right()
    return render(request, 'registration.html', context)


def login(request):
    context = create_content_right()
    return render(request, 'login.html', context)


def profilesettings(request):
    context = create_content_right()
    return render(request, 'profilesettings.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # Или куда-то еще после успешного логина
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')  # Возвращаем пользователя на страницу логина, если ошибка

    return render(request, 'login.html')

def tag(request, tag_label):
    context = create_content(models.Question.objects.get_questions_for_tag(tag_label), request)
    context["tag_label"] = models.Tag.objects.get_tag_by_title(tag_label)
    return render(request, 'tag.html', context)

