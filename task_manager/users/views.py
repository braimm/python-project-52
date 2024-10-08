from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth import get_user_model
#from task_manager.users.models import User
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .forms import RegisterUserForm


# Create your views here.
#class ListUsersView(View):
#    def get(self, request):
#        return render(request, 'users_list.html')
class ListUsersView(ListView):
    model = get_user_model()
    template_name = 'users_list.html'
    context_object_name = 'users'

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
        messages.success(request, 'Пользователь успешно зарегистрирован')
        return render(request, 'login.html')

    

class UpdateUserView(UpdateView):
    def get(self, request, **kwargs):
        return render(request, 'update_user.html')
    

class DeleteUserView(SuccessMessageMixin, DeleteView):
    model = get_user_model()
    template_name = 'delete_user.html'
    success_url = reverse_lazy("list_users")
    success_message = 'Пользователь успешно удален'

