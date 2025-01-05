from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .forms import RegisterUserForm, UpdateUserForm
from django.utils.translation import gettext as _
from task_manager.ext_mixins import NoLogin


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
            # if form.cleaned_data['password'] != form.cleaned_data['password2']:            
            #     context = {
            #         'form': form,
            #         'error': 'Введенные пароли не совпадают.'
            #     }
            #     return render(request, 'create_user.html', context)
            # if len(form.cleaned_data['password']) < 3:            
            #     error = '''
            #         Введённый пароль слишком короткий.
            #         Он должен содержать как минимум 3 символа.
            #     '''
            #     context = {
            #         'form': form,
            #         'error': error
            #     }
            #     return render(request, 'create_user.html', context)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, _('User successfully registered'))
            return redirect('login')
        context = {
            'form': form,
            'err': str(form.errors.as_data().get('password2')[0])[2:-2]
        }
        return render(request, 'create_user.html', context)
        # return render(request, 'create_user.html')
    



class UpdateUserView(NoLogin, UpdateView):
    model = get_user_model()
    form_class = RegisterUserForm
    success_url = reverse_lazy("list_users")
    template_name = 'update_user.html'

    def get(self, request, pk):
        if pk != request.user.pk:
            messages.error(request, _('You do not have permission to modify another user.'))
            return redirect(reverse_lazy('list_users'))
        # return render(request, 'update_user.html')
        return super().get(request, pk)

    def post(self, request, pk):
        form = UpdateUserForm(request.POST)
        print(form.is_valid())
        print(form)
        if form.is_valid():
            user = get_user_model().objects.get(pk=pk)
            user.first_name = form.cleaned_data['first_name'] 
            user.last_name = form.cleaned_data['last_name']
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, _('User successfully updated'))
            return redirect('list_users')
        context = {
            'form': form,
            'err': str(form.errors.as_data().get('password2')[0])[2:-2]
        }
        return render(request, 'update_user.html', context)

    # def post(self, request, pk):
    #     form = UpdateUserForm(request.POST)
    #     print(form.is_valid())
    #     print(form)
    #     if not form.is_valid():
    #         context = {
    #             'form': form,
    #             'err': str(form.errors.as_data().get('password2')[0])[2:-2]
    #         }
    #         return render(request, 'update_user.html', context)
    #     return super().post(request, pk)


# class DeleteUserView(SuccessMessageMixin, DeleteView):
#     model = get_user_model()
#     template_name = 'delete_user.html'
#     success_url = reverse_lazy("list_users")
#     success_message = _('User successfully delete')

class DeleteUserView(NoLogin, View):    
    def get(self, request, pk):
        if request.user.pk != pk:
            messages.error(request, _('You do not have permission to modify another user.'))
            return redirect('list_users')
        return render(request, 'delete_user.html')

    def post(self, request, pk):        
        user = get_user_model().objects.get(pk=pk)
        if user.author.exists() or user.executor.exists():
            messages.error(request, _('Cannot delete user because it is in use'))
            return redirect('list_users')
        user.delete()
        messages.success(request, _('User successfully delete'))
        return redirect('list_users')
