from django.urls import path
from . import views

urlpatterns = [
    path('', views.study_chat, name='study_chat'),
    path('clear/', views.clear_chat, name='clear_study_chat'),
]
