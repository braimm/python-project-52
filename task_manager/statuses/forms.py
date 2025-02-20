from django import forms
from task_manager.statuses.models import Status
from django.utils.translation import gettext as _


class CreateStatusForm(forms.ModelForm):
    name = forms.CharField(max_length=50, label=_('Name'))

    class Meta:
        model = Status
        fields = ['name']
