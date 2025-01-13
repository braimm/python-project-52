# from django_filters import FilterSet
# from django_filters import ChoiceFilter, BooleanFilter

# from django import forms
# from .models import Task
# from task_manager.labels.models import Label

# class TasksFilter(FilterSet):
#     label = ChoiceFilter(
#         choices=lambda: [(label.id, label.name)
#                          for label
#                          in Label.objects.all()],
#         field_name='labels',
#         label= 'Метки',
#     )
#     self_tasks = BooleanFilter(widget=forms.CheckboxInput,
#                                method='filter_author',
#                                label= 'Только свои задачи')

#     def filter_author(self, queryset, *args, **kwargs):
#         author = args[-1]
#         if author:
#             author = getattr(self.request, 'user', None)
#             return queryset.filter(author=author)
#         return queryset

#     class Meta:
#         model = Task
#         fields = ['status', 'executor', 'label', 'self_tasks']

from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter
# from django_filters import ModelMultipleChoiceFilter
from django import forms

from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


class TasksFilter(FilterSet):
    status = ModelChoiceFilter(
        field_name='status',
        queryset=Status.objects.all(),
        label=_('Status')
    )
    executor = ModelChoiceFilter(
        field_name='executor',
        queryset=get_user_model().objects.all(),
        label=_('Executor')
    )
    label = ModelChoiceFilter(
        field_name='labels',
        queryset=Label.objects.all(),
        label=_('Label')
    )
    self_tasks = BooleanFilter(
        field_name='labels',
        widget=forms.CheckboxInput,
        method='filter_author', label=_('Only my tasks')
    )

    def filter_author(self, queryset, name, value):
        attr_user = value
        if attr_user:
            current_user = getattr(self.request, 'user', None)
            return queryset.filter(author=current_user)
        return queryset
    
    class Meta:
        model = Task
        fields = []

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        user = getattr(self.request, 'user', None)
        it_self = self.request.GET.get('self_tasks', None)
        if user and user.is_authenticated:
            if it_self:
                queryset = queryset.filter(author=user)
        return queryset