"""
URL configuration for invera_todo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todo_app.views import UserListView, AllTaskListView, UserTaskListView, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', UserListView.as_view(), name='user-list'),
    path('tasks/', AllTaskListView.as_view(), name='all-tasks'),
    path('tasks/user/', UserTaskListView.as_view(), name='user-tasks'),
    path('register/', RegisterView.as_view(), name='register'),
]
