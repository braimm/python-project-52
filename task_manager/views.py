from django.shortcuts import render
from django.views import View
from django.contrib import messages
from task_manager.forms import LoginUserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

    
# class LoginUserView(View):
#     def get(self, request):
#         return render(request, 'login.html')
#     def post(self, request):
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user and user.is_active:
#                 login(request, user)
#                 messages.success(request, 'Вы залогинены')
#                 return HttpResponseRedirect(reverse('start_page'))
#         messages.error(request, 'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.')
#         return render(request, 'login.html')

class LoginUserView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('start_page')
    success_message = "Вы залогинены"

class LogoutUserView(View):
    def post(self, request):
        logout(request)
        messages.info(request, 'Вы разлогинены')
        return HttpResponseRedirect(reverse('login'))
