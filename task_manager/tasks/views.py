from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.tasks.forms import CreateTaskForm
from task_manager.ext_mixins import NoLogin
from django_filters.views import FilterView
from .filter import TasksFilter
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


# Create your views here.

# class ListTasksView(ListView, FilterView):
#     model = Task
#     template_name = 'list_tasks.html'
#     filterset_class = TasksFilter
#     context_object_name = 'tasks'

# def ListTasksView(request):
#     f = TasksFilter(request.GET, queryset=Task.objects.all())
#     return render(request, 'list_tasks.html', {'filter': f})


# class CreateTaskView(View):
#     def get(self, request):
#         return render(request, 'create_task.html')
#     def post(self, request):
#         form = CreateTaskForm(request.POST)
#         print(form)
#         print(form.is_valid())
#         print(form.errors)
#         #if form.is_valid():
#         form.save()
#         messages.success(request, 'Задача успешно создана')
#         return HttpResponseRedirect(reverse("list_tasks"))
#         #return render(request, 'create_status.html')

class ListTasksView(View):
    template = 'list_tasks.html'

    def get(self, request):
        tasks = Task.objects.all()
        statuses = Status.objects.all()
        executors = get_user_model().objects.all()
        labels = Label.objects.all()
        tasks_filtered = TasksFilter(
            request.GET, queryset=tasks, request=request
        )
        return render(
            request, self.template, {
                'statuses': statuses,
                'executors': executors,
                'labels': labels,
                'filter': tasks_filtered
            }
        )





class CreateTaskView(NoLogin, CreateView):
    form_class = CreateTaskForm
    context_object_name = 'test'
    success_url = reverse_lazy('list_tasks')
    success_message = _('Task successfully created')
    template_name = 'create_task.html'
    context_object_name = 'task'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PageTaskView(NoLogin, DetailView):
    model = Task
    template_name = 'page_task.html'


class UpdateTaskView(NoLogin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = CreateTaskForm
    template_name = 'update_task.html'
    success_url = reverse_lazy("list_tasks")
    success_message = _('Task successfully updated')



class DeleteTaskView(NoLogin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'delete_task.html'
    success_url = reverse_lazy("list_tasks")
    success_message = _('Task successfully deleted')
