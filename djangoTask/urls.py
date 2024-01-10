"""djangoTask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from tasks import views

urlpatterns = [
    path('', views.redirecting, name=""),
    path('admin/', admin.site.urls),
    path('login/', views.login_user, name="login"),
    path('register/', views.register_user, name="register"),
    path('home/', views.home, name="home"),
    path('taskRealizadas/', views.taskRealizadas, name="taskRealizadas"),
    path('taskPendientes/', views.taskPendientes, name="taskPendientes"),
    path('profile/', views.profile, name="profile"),
    path('profile_edit/<int:id>', views.editProfile, name="editProfile"),
    path('profile_delete/<int:id>', views.deleteProfile, name="deleteProfile"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('add_task/', views.add_task, name="add_task"),
    path('view_task/<int:id>', views.taskView, name="taskView"),
    path('task_complete/<int:id>', views.taskComplete, name="taskComplete"),
    path('task_edit/<int:id>', views.editTask, name="editTask"),
    path('task_delete/<int:id>', views.deleteTask, name="deleteTask")
    
]
