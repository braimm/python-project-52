from django_filters import FilterSet
from task_manager.tasks.models import Task


class TasksFilter(FilterSet):
    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']