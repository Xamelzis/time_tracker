from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.utils import timezone
from .models import Task, CategoryTime, CategoryActivity

# Список задач для текущего пользователя
@login_required
def task_list(request):
    # Получаем все категории времени и активности
    category_times = CategoryTime.objects.all()
    category_activities = CategoryActivity.objects.all()
    
    # Получаем задачи текущего пользователя
    tasks = Task.objects.filter(user=request.user)
    
    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'category_times': category_times,
        'category_activities': category_activities,
         })

# Добавление задачи для администратора (для другого пользователя)
@login_required
def add_task_admin(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Получаем пользователя по ID

    if request.method == 'POST':
        title = request.POST.get('title')
        category_time_id = request.POST.get('category_time')  # Получаем категорию времени
        category_activity_id = request.POST.get('category_activity')  # Получаем категорию активности

        # Получаем объекты категорий
        category_time = get_object_or_404(CategoryTime, id=category_time_id)
        category_activity = get_object_or_404(CategoryActivity, id=category_activity_id)

        # Создаем задачу
        Task.objects.create(
            user=user,
            title=title,
            category_time=category_time,
            category_activity=category_activity
        )
        return redirect('user_task_list', user_id=user.id)

    return redirect('user_task_list', user_id=user.id)

# Добавление задачи для текущего пользователя
@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category_time_id = request.POST.get('category_time')
        category_activity_id = request.POST.get('category_activity')

        # Получаем объекты категорий
        category_time = get_object_or_404(CategoryTime, id=category_time_id)
        category_activity = get_object_or_404(CategoryActivity, id=category_activity_id)

        # Создаем задачу
        Task.objects.create(
            user=request.user,
            title=title,
            category_time=category_time,
            category_activity=category_activity
        )
        return redirect('task_list')

    return redirect('task_list')

# Удаление задачи текущего пользователя
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    messages.success(request, 'Задача успешно удалена.')
    return redirect('task_list')

# Удаление задачи администратором
@login_required
def delete_task_admin(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task_user_id = task.user.id
    task.delete()
    messages.success(request, 'Задача успешно удалена.')
    return redirect('user_task_list', user_id=task_user_id)

# Начало выполнения задачи
@login_required
def start_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.started_at = timezone.now()
    task.save()
    messages.success(request, 'Задача начата.')
    return redirect('task_list')

# Завершение задачи
@login_required
def finish_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.finished_at = timezone.now()
    task.completed = True
    task.save()
    messages.success(request, 'Задача завершена.')
    return redirect('task_list')

# Регистрация нового пользователя
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно. Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Список пользователей
@login_required
def users_list(request):
    users = User.objects.filter(is_superuser=False)  # Исключаем суперпользователей
    return render(request, 'users/users_list.html', {'users': users})
    

def is_admin(user):
    return user.is_superuser  # Проверяем, является ли пользователь администратором

@login_required
@user_passes_test(is_admin, login_url='/task_list/')  # Перенаправление для неадминистраторов
def user_tasks(request, user_id):
    user = get_object_or_404(User, id=user_id)
    tasks = Task.objects.filter(user=user)
    category_times = CategoryTime.objects.all()  # Получаем все категории времени
    category_activities = CategoryActivity.objects.all()  # Получаем все категории активностей
    
    return render(request, 'users/user_tasks.html', {
        'user': user,
        'tasks': tasks,
        'category_times': category_times,
        'category_activities': category_activities,
    })

# Управление аккаунтом пользователя
@login_required
def manage_account(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        if 'delete' in request.POST:
            user.delete()
            messages.success(request, 'Аккаунт успешно удален.')
            return redirect('users_list')
        elif 'change_password' in request.POST:
            new_password = request.POST.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Обновляем сессию
            messages.success(request, 'Пароль успешно изменен.')
            return redirect('manage_account', user_id=user.id)

    return render(request, 'users/manage_account.html', {'user': user})
    
def change_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)  # Обновляем сессию
        messages.success(request, 'Пароль успешно изменен.')
        return redirect('manage_account', user_id=user.id)

    return render(request, 'manage_account.html', {'user': user})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Аккаунт успешно удален.')
        return redirect('/admin/auth/user/')  # Перенаправление на список пользователей

    return render(request, 'manage_account.html', {'user': user})
