from django.urls import path
from . import views

urlpatterns = [
    path('habits/', views.habit_list, name='habit-list'),
    path('habits/<int:pk>/', views.habit_detail, name='habit-detail'),
    path('habits/public/', views.public_habits, name='public-habits'),
]