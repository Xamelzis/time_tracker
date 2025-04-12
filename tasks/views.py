
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Task
from django.utils import timezone

@login_required
def task_list(request):
    return render(request, 'tasks/task_list.html')
    
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