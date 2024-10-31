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
from django.urls import path
from task_manager.labels import views

# app_name = "users"

urlpatterns = [
    path('', views.ListLabelsView.as_view(), name='list_labels'),
    path('create/', views.CreateLabelView.as_view(), name='create_label'),
    path('<int:pk>/delete/', views.DeleteLabelView.as_view(), name='delete_label'),
    path('<int:pk>/update/', views.UpdateLabelView.as_view(), name='update_label'),
]