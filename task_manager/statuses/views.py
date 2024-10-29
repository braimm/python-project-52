from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

# Create your views here.

class ListStatusesView(View):
    def get(self, request):
        return render(request, 'statuses.html')
    def post(self, request):
        pass


class CreateStatusView(View):
    pass    


class UpdateStatusView(SuccessMessageMixin, UpdateView):
    pass


class DeleteStatusView(SuccessMessageMixin, DeleteView):
    pass
