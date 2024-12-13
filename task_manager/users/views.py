from django.shortcuts import render,redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .forms import RegisterUserForm
from django.utils.translation import gettext as _


# Create your views here.

class ListUsersView(ListView):
    model = get_user_model()
    template_name = 'list_users.html'
    context_object_name = 'users'

class CreateUserView(View):
    
    def get(self, request):
        return render(request, 'create_user.html')

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, _('User successfully registered'))
            return redirect('login')
        return render(request, 'create_user.html')


class UpdateUserView(SuccessMessageMixin, UpdateView):
    model = get_user_model()
    form_class = RegisterUserForm
    template_name = 'update_user.html'
    success_url = reverse_lazy("list_users")
    success_message = _('User successfully updated')

# class DeleteUserView(SuccessMessageMixin, DeleteView):
#     model = get_user_model()
#     template_name = 'delete_user.html'
#     success_url = reverse_lazy("list_users")
#     success_message = _('User successfully delete')

class DeleteUserView(View):
    
    def get(self, request):
        return render(request, 'delete_user.html')

    def post(self, request):
        user = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, _('User successfully delete'))
            return redirect('list_users')
        return render(request, 'create_user.html')


