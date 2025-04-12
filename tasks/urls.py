from django.urls import path
from django.contrib.auth import views as auth_views
from .views import task_list, add_task, delete_task, start_task, finish_task, register  # Импортируйте необходимые представления
from .views import task_list, add_task, delete_task, start_task, finish_task, register

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
   path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('task_list/', task_list, name='task_list'),
    path('add/', add_task, name='add_task'),
    path('delete/<int:task_id>/', delete_task, name='delete_task'),
    path('start/<int:task_id>/', start_task, name='start_task'),
    path('finish/<int:task_id>/', finish_task, name='finish_task'),
    path('register/', register, name='register'),
]
