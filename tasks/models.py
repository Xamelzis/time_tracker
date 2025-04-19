from django.db import models
from django.contrib.auth.models import User

class CategoryTime(models.Model):
    name = models.CharField(max_length=100)  # Поле для хранения названия категории времени

    def __str__(self):
        return self.name  # Возвращаем название категории для удобства отображения

class CategoryActivity(models.Model):
    name = models.CharField(max_length=100)  

    def __str__(self):
        return self.name  
        
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    category_time = models.ForeignKey(CategoryTime, on_delete=models.SET_NULL, null=True, blank=True)
    category_activity = models.ForeignKey(CategoryActivity, on_delete=models.SET_NULL, null=True, blank=True)

    def duration(self):
        if self.started_at and self.finished_at:
            total_seconds = (self.finished_at - self.started_at).total_seconds()
            hours = int(total_seconds // 3600)  # Получаем количество часов
            minutes = int((total_seconds % 3600) // 60)  # Получаем количество минут
            seconds = int(total_seconds % 60)  # Получаем оставшиеся секунды
            return f"{hours} час(ов) {minutes} минут(ы) {seconds} секунд(ы)"
        return "0 секунд"
        
