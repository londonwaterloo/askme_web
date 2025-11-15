from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ask/', views.ask, name='ask'),
    path('question/<int:q_id>/', views.question_page, name='question'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('profilesettings/', views.profilesettings, name='profile'),
    path('tag/<str:tag_label>/', views.tag, name='tag'),
]
