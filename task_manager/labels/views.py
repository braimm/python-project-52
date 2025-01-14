from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, UpdateView
from task_manager.labels.models import Label
from task_manager.labels.forms import CreateLabelForm
from task_manager.ext_mixins import NoLogin
from django.utils.translation import gettext as _


# Create your views here.


class ListLabelsView(NoLogin, ListView):
    model = Label
    template_name = 'list_labels.html'
    context_object_name = 'labels'


class CreateLabelView(NoLogin, View):
    def get(self, request):
        return render(request, 'create_label.html')

    def post(self, request):
        form = CreateLabelForm(request.POST)
        form.save()
        messages.success(request, _('Label successfully created'))
        return HttpResponseRedirect(reverse("list_labels"))


class UpdateLabelView(NoLogin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = CreateLabelForm
    template_name = 'update_label.html'
    success_url = reverse_lazy("list_labels")
    success_message = _('Label successfully updated')


# class DeleteLabelView(NoLogin, SuccessMessageMixin, DeleteView):
#     model = Label
#     template_name = 'delete_label.html'
#     success_url = reverse_lazy("list_labels")
#     success_message = _('Label successfully deleted')

class DeleteLabelView(NoLogin, View):
    def get(self, request, pk):
        return render(request, 'delete_label.html')

    def post(self, request, pk):
        label = Label.objects.get(pk=pk)
        if label.labels.exists():
            messages.error(
                request,
                _('The label cannot be deleted because it is in use')
            )
            return redirect('list_labels')
        label.delete()
        messages.success(request, _('Label successfully deleted'))
        return redirect('list_labels')
