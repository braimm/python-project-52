from django import forms 
from django.contrib.auth import get_user_model


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    #password2 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
  
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'password']
        #fields = ['first_name', 'last_name', 'username', 'password', 'password2']
        #labels = {
        #    'first_name': 'Имя',
        #    'last_name': 'Фамилия',
        #    'username': 'Имя пользователя',
        #}