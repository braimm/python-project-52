from django import forms 
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class RegisterUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, label=_('First name'))
    last_name = forms.CharField(max_length=150, label=_('Last name'))
    username = forms.CharField(max_length=150, required=True, label=_('User name'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password Confirmation'), widget=forms.PasswordInput)
  
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'password']
