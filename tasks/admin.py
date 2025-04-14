from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html
from .models import Task 

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

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
