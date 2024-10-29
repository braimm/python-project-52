from django.shortcuts import render
from django.views import View
from django.contrib import messages
from task_manager.forms import LoginUserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

# Create your views here.


#path('statuses/', views.StatusesView.as_view(), name='statuses'),
#path('labels/', views.LabelsView.as_view(), name='labels'),
#path('tasks/', views.TasksView.as_view(), name='tasks'),


class ListLabelsView(View):
    def get(self, request):
        return render(request, 'labels.html')
    def post(self, request):
        pass


class CreateLabelView(View):
    pass    


class UpdateLabelView(SuccessMessageMixin, UpdateView):
    pass


class DeleteLabelView(SuccessMessageMixin, DeleteView):
    pass

