"""
URL configuration for SysOpsSuite project.

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
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from login.views import custom_login_view
from Backups.views import backups_view
from config_search.views import config_search_view
from tasks.views import tasks_view, edit_task, complete_task
from dashboard.views import home_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("login/", custom_login_view, name="login"),
    path("dashboard", home_view, name="home"),
    path("dashboard/backups", backups_view, name="backups"),
    path("dashboard/config_search", config_search_view, name="config_search"),
    path("dashboard/tasks", tasks_view, name="task_list"),
    path("edit-task/<int:task_id>/", edit_task, name="edit_task"),
    path("complete-task/<int:task_id>/", complete_task, name="complete_task"),
]
