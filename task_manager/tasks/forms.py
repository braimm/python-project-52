from django import forms
from task_manager.tasks.models import Task
from django.utils.translation import gettext as _


class CreateTaskForm(forms.ModelForm):
    # name = forms.CharField(max_length=50, required=True)
    # description = forms.CharField(max_length=1000)
    # status = forms.CharField(max_length=50, required=True)
    # executor = forms.CharField(max_length=50, required=True)
    # labels = forms.CharField(max_length=50)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executor'].label_from_instance = \
            lambda obj: f"{obj.get_full_name()}"

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {
            'name': _('Name'),
            'description': _('Description'),
            'status': _('Status'),
            'executor': _('Executor'),
            'labels': _('Labels')
        }
