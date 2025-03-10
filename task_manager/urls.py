"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from task_manager import views
from task_manager.views import custom_404, custom_500

urlpatterns = [
    path('', views.IndexView.as_view(), name='start_page'),
    path('admin/', admin.site.urls),
    path('users/', include('task_manager.users.urls')),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('statuses/', include('task_manager.statuses.urls')),
    path('labels/', include('task_manager.labels.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('test-500/', views.test_500_view),
]

handler500 = custom_500
handler404 = custom_404
