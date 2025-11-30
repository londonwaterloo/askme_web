from django.shortcuts import render
from django.core.paginator import Paginator


QUESTIONS = [
        {
            "title": f"Question #{i}",
            "text": f"Question text #{i}",
            "id": i,
            "tags": ["python", "css", "django"],
            "answers": [
                {
                    "text": f"Answer text #{k}",
                } for k in range(20)
            ]
        } for i in range(20)
    ]
TAGS = ["Python", "VK", "Technopark", "VKEducation", "Web"]

USERS = ["superkran", "nastya", "lui_the_dog", "random_boy", "inferniality", "zahar" ]

PER_PAGE = 10


def pagination(objects, request):
    paginator = Paginator(objects, PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page


def index(request):
    context = {
        "content": pagination(QUESTIONS, request),
        "tags": TAGS,
        "users": USERS
    }
    return render(request, 'index.html', context)


def ask(request):
    context = {
        "tags": TAGS,
        "users": USERS
    }
    return render(request, 'question_form.html', context)


def question_page(request, q_id):
    question = QUESTIONS[q_id]
    context = {
        "question": question,
        "tags": TAGS,
        "users": USERS,
        "content": pagination(question["answers"], request)
    }
    return render(request, 'question_page.html', context)


def registration(request):
    context = {
        "tags": TAGS,
        "users": USERS
    }
    return render(request, 'registration.html', context)


def login(request):
    context = {
        "tags": TAGS,
        "users": USERS
    }
    return render(request, 'login.html', context)


def profilesettings(request):
    context = {
        "tags": TAGS,
        "users": USERS
    }
    return render(request, 'profilesettings.html', context)


def tag(request, tag_label):
    questions = []
    for question in QUESTIONS:
        if tag_label in question["tags"]:
            questions.append(question)

    context = {
        "content": pagination(questions, request),
        "tag_label": tag_label,
        "tags": TAGS,
        "users": USERS
    }
    return render(request, 'tag.html', context)