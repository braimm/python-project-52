from django import forms 
from task_manager.statuses.models import Status


class CreateStatusForm(forms.ModelForm):
    name = forms.CharField(max_length=50, label="Имя")
    
    class Meta:
        model = Status
        fields = ['name']
        labels = {
            'name': 'Имя',
        }