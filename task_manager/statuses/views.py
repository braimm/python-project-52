from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, UpdateView
from task_manager.statuses.models import Status
from task_manager.statuses.forms import CreateStatusForm
from task_manager.mixins import NoLogin
from django.utils.translation import gettext as _

# Create your views here.


class ListStatusesView(NoLogin, ListView):
    model = Status
    template_name = 'list_statuses.html'
    context_object_name = 'statuses'


class CreateStatusView(NoLogin, View):
    def get(self, request):
        return render(request, 'create_status.html')

    def post(self, request):
        form = CreateStatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Status successfully created'))
            return HttpResponseRedirect(reverse("list_statuses"))
        return render(request, 'create_status.html')


class UpdateStatusView(NoLogin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = CreateStatusForm
    template_name = 'update_status.html'
    success_url = reverse_lazy("list_statuses")
    success_message = _('Status successfully updated')


class DeleteStatusView(NoLogin, View):
    def get(self, request, pk):
        return render(request, 'delete_status.html')

    def post(self, request, pk):
        status = Status.objects.get(pk=pk)
        if status.status.exists():
            messages.error(
                request,
                _('The status cannot be deleted because it is in use')
            )
            return redirect('list_statuses')
        status.delete()
        messages.success(request, _('Status successfully deleted'))
        return redirect('list_statuses')
