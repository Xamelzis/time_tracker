from django.urls import path
from django.contrib.auth import views as auth_views
from .views import task_list, add_task, delete_task, start_task, finish_task, register,add_task_admin
from .views import users_list, user_tasks, manage_account, delete_task_admin,delete_user,change_password,home

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
   path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('delete/<int:task_id>/', delete_task, name='delete_task'),
    path('users/delete/<int:task_id>/', delete_task_admin, name='delete_task_admin'),
    path('start/<int:task_id>/', start_task, name='start_task'),
    path('finish/<int:task_id>/', finish_task, name='finish_task'),
    path('register/', register, name='register'),
    path('users/', users_list, name='users_list'),
    path('users/<int:user_id>/tasks/', user_tasks, name='user_tasks'),
    path('users/<int:user_id>/manage/', manage_account, name='manage_account'),
    path('users/<int:user_id>/tasks/', user_tasks, name='user_task_list'),  # Для просмотра задач конкретного пользователя
    path('users/<int:user_id>/tasks/add/', add_task_admin, name='add_task_admin'),  # Для добавления задачи
    path('task_list/', task_list, name='task_list'),  # Для просмотра задач текущего пользователя
    path('tasks/add/', add_task, name='add_task'),
    path('users/<int:user_id>/change_password/', change_password, name='change_password'),
    path('users/<int:user_id>/delete/', delete_user, name='delete_user'),
    path('', home, name='home'),  # Главная страница
]
