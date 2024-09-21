from django.shortcuts import render
from django.views import View
from django.contrib import messages

class IndexView(View):

    def get(self, request):
        return render(request, 'index.html')

    
class LoginUserView(View):
    def get(self, request):
        return render(request, 'login.html')
