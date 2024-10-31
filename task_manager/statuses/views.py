from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from task_manager.statuses.models import Status

# Create your views here.

#class ListStatusesView(View):
#    def get(self, request):
#        return render(request, 'list_statuses.html')
#    def post(self, request):
#        pass


class ListStatusesView(ListView):
    model = Status
    template_name = 'list_statuses.html'
    context_object_name = 'statuses'


class CreateStatusView(View):
   def get(self, request):
       return render(request, 'create_status.html')
   def post(self, request):
       pass


class UpdateStatusView(SuccessMessageMixin, UpdateView):
    pass


class DeleteStatusView(SuccessMessageMixin, DeleteView):
    pass
