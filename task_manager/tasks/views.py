from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, UpdateView
from task_manager.tasks.models import Task
from task_manager.tasks.forms import CreateTaskForm
from task_manager.mixins import NoLogin
from .filter import TasksFilter
from django.utils.translation import gettext as _


# Create your views here.


class ListTasksView(NoLogin, View):
    def get(self, request):
        tasks = Task.objects.all()
        tasks_filtered = TasksFilter(
            request.GET, queryset=tasks, request=request
        )
        return render(
            request, 'tasks/list_tasks.html', {
                'filter': tasks_filtered
            }
        )


class CreateTaskView(NoLogin, SuccessMessageMixin, CreateView):
    form_class = CreateTaskForm
    template_name = 'tasks/create_task.html'
    context_object_name = 'task'
    success_url = reverse_lazy('list_tasks')
    success_message = _('Task successfully created')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PageTaskView(NoLogin, DetailView):
    model = Task
    template_name = 'tasks/page_task.html'


class UpdateTaskView(NoLogin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = CreateTaskForm
    template_name = 'tasks/update_task.html'
    success_url = reverse_lazy("list_tasks")
    success_message = _('Task successfully updated')


class DeleteTaskView(NoLogin, View):
    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        if task.author != request.user:
            messages.error(
                request,
                _('A task can only be deleted by its author')
            )
            return redirect('list_tasks')
        return render(request, 'tasks/delete_task.html', {"task": task})

    def post(self, request, pk):
        task = Task.objects.get(pk=pk)
        task.delete()
        messages.success(request, _('Task successfully deleted'))
        return redirect('list_tasks')
