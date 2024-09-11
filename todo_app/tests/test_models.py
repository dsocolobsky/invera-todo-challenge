from django.test import TestCase
from django.contrib.auth import get_user_model
from todo_app.models import Task

User = get_user_model()


class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_create_task(self):
        task = Task.objects.create(
            user=self.user,
            title="Test Task",
            details="This is a test task",
        )
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.user, self.user)
        self.assertFalse(task.completed)

    def test_task_str_representation(self):
        task = Task.objects.create(
            user=self.user,
            title="Test Task",
            details="This is a test task",
            completed=False,
        )
        self.assertEqual(str(task), "Test Task")
