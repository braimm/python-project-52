from django.forms import CharField, PasswordInput
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class CustomLoginUserForm(AuthenticationForm):
    username = CharField(label=_('User name'))
    password = CharField(label=_('Password'), widget=PasswordInput)
