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

class ListTasksView(View):
    def get(self, request):
        return render(request, 'tasks.html')
    def post(self, request):
        pass


class CreateTaskView(View):
    pass    


class UpdateTaskView(SuccessMessageMixin, UpdateView):
    pass


class DeleteTaskView(SuccessMessageMixin, DeleteView):
    pass
