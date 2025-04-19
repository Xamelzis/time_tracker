from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html
from .models import Task, CategoryTime, CategoryActivity  # Импортируем модели категорий

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'view_tasks_link', 'manage_account_link')

    def view_tasks_link(self, obj):
        url = reverse('user_tasks', args=[obj.id])
        return format_html('<a href="{}">Список задач</a>', url)
    view_tasks_link.short_description = 'Задачи'

    def manage_account_link(self, obj):
        url = reverse('manage_account', args=[obj.id])
        return format_html('<a href="{}">Управление аккаунтом</a>', url)
    manage_account_link.short_description = 'Управление'

# Убираем стандартную регистрацию модели User и заменяем её на кастомную
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Регистрация модели Task
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'started_at', 'finished_at', 'completed')
    list_filter = ('completed', 'started_at', 'finished_at')
    search_fields = ('title', 'user__username')

# Регистрация модели CategoryTime
@admin.register(CategoryTime)
class CategoryTimeAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Отображаем только поле "name"
    search_fields = ('name',)  # Добавляем возможность поиска по названию

# Регистрация модели CategoryActivity
@admin.register(CategoryActivity)
class CategoryActivityAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Отображаем только поле "name"
    search_fields = ('name',)  # Добавляем возможность поиска по названию
