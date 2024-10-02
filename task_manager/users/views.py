from django.shortcuts import render
from django.views import View
from django.contrib import messages
from .forms import RegisterUserForm


# Create your views here.
class UsersView(View):
    def get(self, request):
        return render(request, 'users.html')


class CreateUsersView(View):
    def get(self, request):
        return render(request, 'reg_users.html')

    def post(self, request):
        form = RegisterUserForm(request.POST)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()        
        return render(request, 'login.html')

    

class UpdateUserView(View):
    def get(self, request, **kwargs):
        return render(request, 'update_user.html')
    

class DeleteUserView(View):
    def get(self, request, **kwargs):
        return render(request, 'delete_user.html')

