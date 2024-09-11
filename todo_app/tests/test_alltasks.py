from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from todo_app.models import Task
from rest_framework.authtoken.models import Token

User = get_user_model()


class AllTaskListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpass123"
        )
        self.normal_user = User.objects.create_user(
            username="normaluser", email="normal@example.com", password="normalpass123"
        )
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.normal_token = Token.objects.create(user=self.normal_user)
        self.url = "/all-tasks/"

        Task.objects.create(
            user=self.admin_user,
            title="Admin Task 1",
            details="Admin task details",
            completed=False,
        )
        Task.objects.create(
            user=self.admin_user,
            title="Admin Task 2",
            details="Another admin task",
            completed=True,
        )
        Task.objects.create(
            user=self.normal_user,
            title="User Task 1",
            details="User task details",
            completed=False,
        )

    def test_admin_can_view_all_tasks(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token.key}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Task.objects.count())

    def test_normal_user_cannot_view_all_tasks(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.normal_token.key}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_view_all_tasks(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_all_tasks_content(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token.key}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        for task in response.data:
            self.assertIn("id", task)
            self.assertIn("title", task)
            self.assertIn("details", task)
            self.assertIn("completed", task)
            self.assertIn("user", task)
