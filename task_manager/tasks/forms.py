from django import forms 
from task_manager.tasks.models import Task


class CreateTaskForm(forms.ModelForm):
    #name = forms.CharField(max_length=50, required=True)
    #description = forms.CharField(max_length=1000)
    #author = forms.CharField(max_length=50)
    #status = forms.CharField(max_length=50, required=True)
    #executor = forms.CharField(max_length=50, required=True)
    #labels = forms.CharField(max_length=50)

    
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'status': 'Cтатус',
            'executor': 'Исполнитель',
            'labels': 'Метки'
        }