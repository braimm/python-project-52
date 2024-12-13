from django import forms 
from task_manager.labels.models import Label
from django.utils.translation import gettext as _


class CreateLabelForm(forms.ModelForm):
    name = forms.CharField(max_length=50, label="_('Name')")
    
    class Meta:
        model = Label
        fields = ['name']
        