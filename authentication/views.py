from authentication.forms import ProfileCreationForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.views import View


@method_decorator(csrf_exempt, name='dispatch')
class SignUp(View):
    def get(self, request):
        form = ProfileCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = ProfileCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('common:index')
        return render(request, 'registration/signup.html', {'form': form})
