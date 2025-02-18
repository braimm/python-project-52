from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import re

SHORT_PASSWORD_MSG = _('The password you entered is too short. \
                       It must contain at least 3 characters.')
PASS_NO_MATCH_MSG = _('The passwords entered do not match.')


class RegisterUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, label=_('First name'))
    last_name = forms.CharField(max_length=150, label=_('Last name'))
    username = forms.CharField(
        max_length=150,
        required=True,
        label=_('User name')
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label=_('Password Confirmation'),
        widget=forms.PasswordInput
    )

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'password1']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password1') and cd.get('password1') != cd.get('password2'):
            raise forms.ValidationError(PASS_NO_MATCH_MSG)
        if len(cd['password2']) < 3:
            raise forms.ValidationError(SHORT_PASSWORD_MSG)
        return cd['password2']


class UpdateUserForm(forms.Form):
    first_name = forms.CharField(max_length=150, label=_('First name'))
    last_name = forms.CharField(max_length=150, label=_('Last name'))
    username = forms.CharField(
        max_length=150,
        required=True,
        label=_('User name')
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label=_('Password Confirmation'),
        widget=forms.PasswordInput
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[\w.@+-]+$', username):
            message = _(
                'Please enter a valid username. \
                    It can only contain letters, numbers and @/./+/-/_ signs.')
            raise forms.ValidationError(message)
        return username

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password1') and cd.get('password1') != cd.get('password2'):
            raise forms.ValidationError(PASS_NO_MATCH_MSG)
        if len(cd['password2']) < 3:
            raise forms.ValidationError(SHORT_PASSWORD_MSG)
        return cd['password2']
