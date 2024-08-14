from django.shortcuts import render
from django.views import View

class IndexView(View):

    def get(self, request):
        return render(request, 'index.html')

class CreateUsersView(View):
    def get(self, request):
        return render(request, 'reg_users.html')
    
class LoginUserView(View):
    def get(self, request):
        return render(request, 'login.html')

class UsersView(View):
    def get(self, request):
        return render(request, 'users.html')

