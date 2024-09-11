from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status
from todo_app.models import Task
from datetime import timedelta
from django.utils import timezone

User = get_user_model()


class UserTaskListViewTests(TestCase):
    def setUp(self):
        Task.objects.all().delete()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client = APIClient(HTTP_AUTHORIZATION=f"Bearer {self.token.key}")

        self.task1 = Task.objects.create(
            user=self.user, title="Task 1", details="Important task"
        )
        self.task2 = Task.objects.create(
            user=self.user, title="Task 2", details="Urgent task"
        )
        self.task3 = Task.objects.create(
            user=self.user, title="Task 3", details="Normal task", completed=True
        )

        self.other_user = User.objects.create_user(
            username="otheruser", password="otherpass123"
        )
        self.other_task = Task.objects.create(
            user=self.other_user, title="Other Task", details="Some other task"
        )

    def test_get_all_user_tasks(self):
        self.assertEqual(Task.objects.count(), 4)

        response = self.client.get("/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_tasks(self):
        self.assertEqual(Task.objects.count(), 4)

        data = {
            "title": "New Task",
            "details": "This is a new task",
        }
        response = self.client.post("/tasks/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Task")
        self.assertEqual(response.data["details"], "This is a new task")
        self.assertEqual(response.data["completed"], False)
        self.assertEqual(Task.objects.count(), 5)
        # Ensure tasks are created on this user and not another one
        self.assertEqual(Task.objects.filter(user=self.user).count(), 4)
        self.assertEqual(Task.objects.filter(user=self.other_user).count(), 1)

    def test_create_task_unauthenticated_should_fail(self):
        self.assertEqual(Task.objects.count(), 4)
        self.client = APIClient()
        data = {
            "title": "New Task",
            "details": "This is a new task",
        }
        response = self.client.post("/tasks/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Task.objects.count(), 4)

    def test_filter_by_completed(self):
        response = self.client.get("/tasks/?completed=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Task 3")

    def test_filter_by_title(self):
        response = self.client.get("/tasks/?title=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Task 1")

    def test_filter_by_description(self):
        response = self.client.get("/tasks/?details=Urgent")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Task 2")

    def test_filter_by_date(self):
        old_date = timezone.now() - timedelta(days=365)
        Task.objects.filter(id=self.task1.id).update(created_at=old_date)

        now = timezone.now() - timedelta(minutes=1)
        response = self.client.get(f"/tasks/?created_at_after=2024-01-01")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_unauthenticated_request(self):
        self.client = APIClient()
        response = self.client.get("/tasks/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
