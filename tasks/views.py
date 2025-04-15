
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Task
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

@login_required
def task_list(request):
    return render(request, 'tasks/task_list.html')
    
@login_required
def add_task_admin(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Получаем пользователя по ID

    if request.method == 'POST':
        title = request.POST.get('title')
        Task.objects.create(user=user, title=title)  # Создаем задачу для конкретного пользователя
        return redirect('user_task_list', user_id=user.id)  # Перенаправляем на страницу задач этого пользователя

    return redirect('user_task_list', user_id=user.id)  # Если метод не POST, перенаправляем на страницу задач
    
@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        Task.objects.create(user=request.user, title=title)
        return redirect('task_list')

@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.delete()
    return redirect('task_list')

@login_required
def delete_task_admin(request, task_id):
    try:
        task = Task.objects.get(id=task_id)  # Получаем задачу по ID
        task_user_id = task.user.id  # Получаем ID пользователя, которому принадлежит задача
        task.delete()  # Удаляем задачу
        messages.success(request, 'Задача успешно удалена.')  # Уведомление об успешном удалении
    except Task.DoesNotExist:
        messages.error(request, 'Задача не найдена.')  # Уведомление об ошибке, если задача не найдена
        return redirect('task_list')  # Перенаправляем на страницу задач, если задача не найдена

    return redirect('user_task_list', user_id=task_user_id)  # Перенаправляем на страницу задач пользователя
   
@login_required
def start_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.started_at = timezone.now()
    task.save()
    return redirect('task_list')

@login_required
def finish_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.finished_at = timezone.now()
    task.completed = True
    task.save()
    return redirect('task_list')
    
    from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Перенаправление на страницу входа после успешной регистрации
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
    
# Список пользователей
def users_list(request):
    users = User.objects.filter(is_superuser=False)  # Исключаем суперпользователей
    return render(request, 'users/users_list.html', {'users': users})

# Список задач для конкретного пользователя
def user_tasks(request, user_id):
    user = get_object_or_404(User, id=user_id)
    tasks = Task.objects.filter(user=user)
    return render(request, 'users/user_tasks.html', {'user': user, 'tasks': tasks})

# Управление аккаунтом
def manage_account(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            user.delete()
            messages.success(request, 'Аккаунт успешно удален.')
            return redirect('users/users_list')
        elif 'change_password' in request.POST:
            new_password = request.POST.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Обновляем сессию
            messages.success(request, 'Пароль успешно изменен.')
            return redirect('users/manage_account', user_id=user.id)

    return render(request, 'users/manage_account.html', {'user': user})