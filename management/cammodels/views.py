from crm.forms import CamModelForm, CamModelImageFormset, CamModelFilterForm, ProfileWebsiteFormset
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from crm.models import CamModel, ProfileWebsite
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
import os


@method_decorator(csrf_exempt, name='dispatch')
class CamModelList(LoginRequiredMixin, View):
    def get(self, request):
        filter_form = CamModelFilterForm(request.GET or None)
        models_list = CamModel.objects.all().order_by('-created_at')
        if filter_form.is_valid():
            if filter_form.cleaned_data['name']:
                models_list = models_list.filter(name__icontains=filter_form.cleaned_data['name']).order_by('-created_at')
            if filter_form.cleaned_data['city']:
                models_list = models_list.filter(city=filter_form.cleaned_data['city']).order_by('-created_at')
            if filter_form.cleaned_data['website']:
                models_list = models_list.filter(websites__website=filter_form.cleaned_data['website']).order_by('-created_at')
        paginator = Paginator(models_list, 20)
        page_number = int(request.GET.get('page', 1))
        page_obj = paginator.get_page(page_number)
        page_range = paginator.page_range
        if paginator.num_pages > 15:
            page_range = list(paginator.page_range[max(0, page_number - 7): page_number])
            page_range.extend(paginator.page_range[page_number: min(page_number + 7, paginator.num_pages)])
        return render(request, 'management/cammodel/cammodel_list.html', {'models_list': page_obj, 'page_range': page_range, 'filter_form': filter_form})


@method_decorator(csrf_exempt, name='dispatch')
class CamModelDetail(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        if pk:
            cammodel = CamModel.objects.get(id=pk)
            return render(request, 'management/cammodel/cammodel_detail.html', {'cammodel': cammodel})
        return HttpResponse(status=404)


@method_decorator(csrf_exempt, name='dispatch')
class CamModelCreate(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        form = CamModelForm()
        image_formset = CamModelImageFormset()
        website_formset = ProfileWebsiteFormset(queryset=ProfileWebsite.objects.none())
        if pk:
            cammodel = CamModel.objects.get(id=pk)
            form = CamModelForm(instance=cammodel)
            image_formset = CamModelImageFormset(instance=cammodel)
            website_formset = ProfileWebsiteFormset(queryset=cammodel.websites.all())
        return render(request, 'management/cammodel/cammodel_form.html', {'form': form, 'image_formset': image_formset, 'website_formset': website_formset})

    def post(self, request, pk=None):
        form = CamModelForm(request.POST or None, request.FILES or None)
        images = CamModelImageFormset(request.POST or None, request.FILES or None)
        websites = ProfileWebsiteFormset(request.POST or None)
        if pk:
            instance = CamModel.objects.get(id=pk)
            form = CamModelForm(request.POST or None, request.FILES or None, instance=instance)
            images = CamModelImageFormset(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            cammodel = form.save()
            for image in images:
                if image.is_valid():
                    if 'DELETE' in image.cleaned_data and image.cleaned_data['DELETE']:
                        if image.cleaned_data['id']:
                            if os.path.exists(image.cleaned_data['id'].image.path):
                                os.remove(image.cleaned_data['id'].image.path)
                            image.cleaned_data['id'].delete()
                        continue
                    if image.empty_permitted and not image.has_changed():
                        continue
                    image_instance = image.save(commit=False)
                    image_instance.cammodel = cammodel
                    image_instance.save()
            for website in websites:
                if website.is_valid():
                    if 'DELETE' in website.cleaned_data and website.cleaned_data['DELETE']:
                        if website.cleaned_data['id']:
                            website.cleaned_data['id'].delete()
                        continue
                    if website.empty_permitted and not website.has_changed():
                        continue
                    website_instance = website.save()
                    cammodel.websites.add(website_instance)
            url = reverse('management:cammodel:index')
            if request.GET:
                url += '?' + request.GET.urlencode()
            return redirect(url)
        return render(request, 'management/cammodel/cammodel_form.html', {'form': form, 'image_formset': images, 'website_formset': websites})


@login_required
@csrf_exempt
def cammodel_remove(request, pk):
    url = reverse('management:cammodel:index')
    if request.GET:
        url += '?' + request.GET.urlencode()
    if pk:
        model = CamModel.objects.get(pk=pk)
        # if model.images:
        #     for image in model.images.all():
        #         if os.path.exists(image.image.path):
        #             os.remove(image.image.path)
        # if model.passport_scan:
        #     if os.path.exists(model.passport_scan.path):
        #         os.remove(model.passport_scan.path)
        model.delete()
    return redirect(url)
