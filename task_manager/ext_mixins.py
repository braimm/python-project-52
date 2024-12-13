from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class NoLogin(LoginRequiredMixin):
    login_url = 'login'

    def get_login_url(self):
        messages.error(self.request, "Вы не авторизованы! Пожалуйста, выполните вход.")
        return super().get_login_url()