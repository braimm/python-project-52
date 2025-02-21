from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import RegisterUserForm, UpdateUserForm
from django.utils.translation import gettext as _
from task_manager.mixins import NoLogin
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.

class ListUsersView(ListView):
    model = get_user_model()
    template_name = 'users/list_users.html'
    context_object_name = 'users'


class CreateUserView(View, SuccessMessageMixin):
    success_message = _('User successfully registered')

    def get(self, request):
        return render(request, 'users/create_user.html')

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            # messages.success(request, _('User successfully registered'))
            return redirect('login')
        username = request.POST.get('username')
        return render(
            request,
            'users/create_user.html',
            {'form': form, 'username': username}
        )


class UpdateUserView(NoLogin, UpdateView, SuccessMessageMixin):
    model = get_user_model()
    form_class = RegisterUserForm
    success_url = reverse_lazy("list_users")
    template_name = 'users/update_user.html'
    success_message = _('User successfully updated')

    def get(self, request, pk):
        if pk != request.user.pk:
            messages.error(
                request,
                _('You do not have permission to modify another user.')
            )
            return redirect(reverse_lazy('list_users'))
        return super().get(request, pk)

    def post(self, request, pk):
        form = UpdateUserForm(request.POST)
        input_username = request.POST.get('username')
        current_username = request.user.username
        is_conflict_username = False
        if current_username != input_username:
            is_conflict_username = get_user_model().objects.\
                filter(username=input_username).exists()

        if form.is_valid() and not is_conflict_username:
            user = get_user_model().objects.get(pk=pk)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password1'])
            user.save()
            # messages.success(request, _('User successfully updated'))
            return redirect('list_users')
        if is_conflict_username:
            form.add_error(
                'username',
                _('A user with this name already exists.')
            )

        return render(
            request,
            'users/update_user.html',
            {'form': form, 'username': input_username}
        )


class DeleteUserView(NoLogin, View, SuccessMessageMixin):
    success_message = _('User successfully delete')

    def get(self, request, pk):
        if request.user.pk != pk:
            messages.error(
                request,
                _('You do not have permission to modify another user.')
            )
            return redirect('list_users')
        return render(request, 'users/delete_user.html')

    def post(self, request, pk):
        user = get_user_model().objects.get(pk=pk)
        if user.author.exists() or user.executor.exists():
            messages.error(
                request,
                _('Cannot delete user because it is in use')
            )
            return redirect('list_users')
        user.delete()
        # messages.success(request, _('User successfully delete'))
        return redirect('list_users')
