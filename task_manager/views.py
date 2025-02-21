from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CustomLoginUserForm
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseServerError


def custom_500(request):
    return render(request, 'errors/500.html', status=500)


def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)


def test_500_view(request):
    raise HttpResponseServerError("Тестовая ошибка 500!")


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class LoginUserView(SuccessMessageMixin, LoginView):
    form_class = CustomLoginUserForm
    template_name = 'login.html'
    next_page = reverse_lazy('start_page')
    success_message = _('You are logged in')


class LogoutUserView(View):
    def post(self, request):
        logout(request)
        messages.info(request, _('You are logged out'))
        return HttpResponseRedirect(reverse('start_page'))
