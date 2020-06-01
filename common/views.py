from crm.forms import CamModelRequestForm, CamModelRequestImageFormset
from authentication.forms import ProfileCreationForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
import uuid


@method_decorator(csrf_exempt, name='dispatch')
class Index(View):
    def get(self, request):
        # form = ProfileCreationForm()
        return render(request, 'index.html')

    # def post(self, request):
    #     form = ProfileCreationForm(request.POST or None)
    #     if form.is_valid():
    #         form.save()
    #         email = request.POST['email']
    #         password = request.POST['password1']
    #         user = authenticate(email=email, password=password)
    #         if user is not None:
    #             login(request, user)
    #             return redirect('management:index')
    #         else:
    #             return redirect('authentication:login')
    #     else:
    #         return render(request, 'registration/signup.html', {'form': form})


@method_decorator(csrf_exempt, name='dispatch')
class ModelRequest(View):
    def get(self, request):
        form = CamModelRequestForm()
        formset = CamModelRequestImageFormset()
        return render(request, 'model_request/model_request_form.html', {'form': form, 'formset': formset})

    def post(self, request):
        form = CamModelRequestForm(request.POST or None, request.FILES or None)
        formset = CamModelRequestImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid():
            cammodel_request = form.save()
            for image in formset:
                if image.is_valid():
                    if 'DELETE' in image.cleaned_data and image.cleaned_data['DELETE']:
                        if image.cleaned_data['id']:
                            image.cleaned_data['id'].delete()
                        continue
                    if image.empty_permitted and not image.has_changed():
                        continue
                    image_instance = image.save(commit=False)
                    image_instance.request = cammodel_request
                    image_instance.save()
            # cammodel_request.request_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, cammodel_request.name)
            # cammodel_request.save()
            messages.success(request, 'Заявка принята. С вами свяжутся по указанному вами номеру или почте. Спасибо.')
            return redirect('common:index')
        else:
            messages.error(request, f'Произошла ошибка. {form.errors}')
            return render(request, 'model_request/model_request_form.html', {'form': form, 'formset': formset})
