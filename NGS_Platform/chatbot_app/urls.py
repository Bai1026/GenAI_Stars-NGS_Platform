from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit_user_info/', views.submit_user_info, name='submit_user_info'),
    path('chat/', views.chat, name='chat'),
]
