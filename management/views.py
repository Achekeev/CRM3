from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import View


@method_decorator(csrf_exempt, name='dispatch')
class Management(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'management/management.html')
