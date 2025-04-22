import pytest
from tasks.models import CategoryTime, CategoryActivity, Task
from django.contrib.auth.models import User
from datetime import datetime, timedelta

@pytest.mark.django_db
def test_category_time_creation():
    category = CategoryTime.objects.create(name="Work")
    assert category.name == "Work"
    assert str(category) == "Work"

@pytest.mark.django_db
def test_category_activity_creation():
    category = CategoryActivity.objects.create(name="Programming")
    assert category.name == "Programming"
    assert str(category) == "Programming"

@pytest.mark.django_db
def test_task_creation():
    user = User.objects.create_user(username="testuser", password="password")
    category_time = CategoryTime.objects.create(name="Work")
    category_activity = CategoryActivity.objects.create(name="Programming")
    
    task = Task.objects.create(
        user=user,
        title="Test Task",
        started_at=datetime.now(),
        finished_at=datetime.now() + timedelta(hours=1),
        completed=True,
        category_time=category_time,
        category_activity=category_activity
    )
    
    assert task.title == "Test Task"
    assert task.completed is True
    assert task.category_time.name == "Work"
    assert task.category_activity.name == "Programming"

@pytest.mark.django_db
def test_task_duration():
    user = User.objects.create_user(username="testuser", password="password")
    task = Task.objects.create(
        user=user,
        title="Test Task",
        started_at=datetime(2025, 4, 22, 10, 0, 0),
        finished_at=datetime(2025, 4, 22, 12, 30, 45),
        completed=True
    )
    
    assert task.duration() == "2 час(ов) 30 минут(ы) 45 секунд(ы)"
