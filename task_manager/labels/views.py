from django.shortcuts import render
from django.views import View
from django.contrib import messages
from task_manager.forms import LoginUserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from task_manager.labels.models import Label
from task_manager.labels.forms import CreateLabelForm

# Create your views here.


class ListLabelsView(ListView):
    model = Label
    template_name = 'list_labels.html'
    context_object_name = 'labels'


class CreateLabelView(View):
    def get(self, request):
        return render(request, 'create_label.html')
    def post(self, request):
        form = CreateLabelForm(request.POST)
        form.save()
        messages.success(request, 'Метка успешно создана')
        return HttpResponseRedirect(reverse("list_labels"))
        #return render(request, 'create_status.html')

class UpdateLabelView(SuccessMessageMixin, UpdateView):
    pass


class DeleteLabelView(SuccessMessageMixin, DeleteView):
    pass

