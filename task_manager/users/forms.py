from django import forms 
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import re


class RegisterUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, label=_('First name'))
    last_name = forms.CharField(max_length=150, label=_('Last name'))
    username = forms.CharField(max_length=150, required=True, label=_('User name'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password Confirmation'), widget=forms.PasswordInput)
  
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'password']
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') and cd.get('password') != cd.get('password2'):
            raise forms.ValidationError("Введенные пароли не совпадают.")
        if len(cd['password2']) < 3:
            raise forms.ValidationError("Введённый пароль слишком короткий. Он должен содержать как минимум 3 символа.")
        return cd['password2']


class UpdateUserForm(forms.Form):
    first_name = forms.CharField(max_length=150, label=_('First name'))
    last_name = forms.CharField(max_length=150, label=_('Last name'))
    username = forms.CharField(max_length=150, required=True, label=_('User name'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password Confirmation'), widget=forms.PasswordInput)
  
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[\w.@+-]+$', username):
            raise forms.ValidationError('Введите правильное имя пользователя. Оно может содержать только буквы, цифры и знаки @/./+/-/_')
        return username
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') and cd.get('password') != cd.get('password2'):
            raise forms.ValidationError("Введенные пароли не совпадают.")
        if len(cd['password2']) < 3:
            raise forms.ValidationError("Введённый пароль слишком короткий. Он должен содержать как минимум 3 символа.")
        return cd['password2']