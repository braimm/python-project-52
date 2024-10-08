from django.shortcuts import render
from django.views import View
from django.contrib import messages
from task_manager.forms import LoginUserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

    
class LoginUserView(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                messages.success(request, 'Вы залогинены')
                return HttpResponseRedirect(reverse('start_page'))
        return render(request, 'login.html')

class LogoutUserView(View):
    def post(self, request):
        logout(request)
        messages.success(request, 'Вы разлогинены')
        return HttpResponseRedirect(reverse('login'))

class StatusesView(View):
    def get(self, request):
        return render(request, 'statuses.html')
    def post(self, request):
        pass

class LabelsView(View):
    def get(self, request):
        return render(request, 'labels.html')
    def post(self, request):
        pass

class TasksView(View):
    def get(self, request):
        return render(request, 'tasks.html')
    def post(self, request):
        pass

