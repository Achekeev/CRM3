from crm.forms import CamModelRequestForm, CamModelRequestImageFormset
from crm.models import CamModelRequest, CamModel, CamModelImage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
import os


@method_decorator(csrf_exempt, name='dispatch')
class CamModelRequestList(LoginRequiredMixin, View):
    def get(self, request):
        requests = CamModelRequest.objects.all().order_by('-created_at')
        paginator = Paginator(requests, 20)
        page_number = int(request.GET.get('page', 1))
        page_obj = paginator.get_page(page_number)
        page_range = paginator.page_range
        if paginator.num_pages > 15:
            page_range = list(paginator.page_range[max(0, page_number - 7): page_number])
            page_range.extend(paginator.page_range[page_number: min(page_number + 7, paginator.num_pages)])
        return render(request, 'management/cammodelrequests/cammodelrequests.html', {'requests': page_obj, 'page_range': page_range})


@method_decorator(csrf_exempt, name='dispatch')
class CamModelRequestDetail(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        if pk:
            cammodelrequest = CamModelRequest.objects.get(id=pk)
            images = cammodelrequest.images.all()
            return render(request, 'management/cammodelrequests/cammodelrequest_detail.html', {'cammodelrequest': cammodelrequest, 'images': images})
        return HttpResponse(status=404)


@method_decorator(csrf_exempt, name='dispatch')
class CamModelRequestCreateNewModel(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        if pk:
            cammodelrequest = CamModelRequest.objects.get(id=pk)
            form = CamModelRequestForm(instance=cammodelrequest)
            formset = CamModelRequestImageFormset(instance=cammodelrequest)
            return render(request, 'management/cammodelrequests/cammodelrequest_form.html', {'form': form, 'formset': formset})
        else:
            return HttpResponse(status=404)

    def post(self, request, pk=None):
        form = CamModelRequestForm(request.POST or None, request.FILES or None)
        formset = CamModelRequestImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid():
            kwargs = {
                'name': form.cleaned_data['name'],
                'description': form.cleaned_data['description'],
                'schedule': form.cleaned_data['schedule'],
                'phone': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'contacts': form.cleaned_data['contacts'],
                'login': form.cleaned_data['login'],
                'password': form.cleaned_data['password'],
            }
            cammodel = CamModel.objects.create(**kwargs)
            if pk:
                cammodelrequest = CamModelRequest.objects.get(id=pk)
                cammodel.passport_scan = cammodelrequest.passport_scan
                for image in cammodelrequest.images.all():
                    CamModelImage.objects.create(image=image.image, cammodel=cammodel)
            cammodel.save()
            # for image in formset:
            #     if image.is_valid():
            #         if 'DELETE' in image.cleaned_data and image.cleaned_data['DELETE']:
            #             if image.cleaned_data['id']:
            #                 image.cleaned_data['id'].delete()
            #             continue
            #         if image.empty_permitted and not image.has_changed():
            #             continue
            #         image_instance = image.save(commit=False)
            #         image_instance.request = cammodel
            #         image_instance.save()
            url = reverse('management:cammodel:index')
            if request.GET:
                url += '?' + request.GET.urlencode()
            return redirect(url)
        return render(request, 'management/cammodelrequests/cammodelrequest_form.html', {'form': form, 'formset': formset})


@login_required
@csrf_exempt
def cammodelrequest_remove(request, pk):
    url = reverse('management:cammodelrequest:index')
    if request.GET:
        url += '?' + request.GET.urlencode()
    if pk:
        model = CamModelRequest.objects.get(pk=pk)
        if model.images:
            for image in model.images.all():
                if os.path.exists(image.image.path):
                    os.remove(image.image.path)
        if model.passport_scan:
            if os.path.exists(model.passport_scan.path):
                os.remove(model.passport_scan.path)
        model.delete()
    return redirect(url)
