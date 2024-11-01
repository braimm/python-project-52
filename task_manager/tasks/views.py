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
from task_manager.tasks.models import Task
from task_manager.tasks.forms import CreateTaskForm

# Create your views here.

class ListTasksView(ListView):
    model = Task
    template_name = 'list_tasks.html'
    context_object_name = 'tasks'


class CreateTaskView(View):
    def get(self, request):
        return render(request, 'create_task.html')
    def post(self, request):
        form = CreateTaskForm(request.POST)
        print(form)
        print(form.is_valid())
        print(form.errors)
        #if form.is_valid():
        form.save()
        messages.success(request, 'Задача успешно создана')
        return HttpResponseRedirect(reverse("list_tasks"))
        #return render(request, 'create_status.html')

class PageTaskView(View):
    pass


class UpdateTaskView(SuccessMessageMixin, UpdateView):
    pass


class DeleteTaskView(SuccessMessageMixin, DeleteView):
    pass
