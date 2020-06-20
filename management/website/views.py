from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from crm.forms import WebsiteForm
from django.urls import reverse
from crm.models import Website
from django.views import View


@method_decorator(csrf_exempt, name='dispatch')
class WebsiteList(LoginRequiredMixin, View):
    def get(self, request):
        website_list = Website.objects.all()
        paginator = Paginator(website_list, 20)
        page_number = int(request.GET.get('page', 1))
        page_obj = paginator.get_page(page_number)
        page_range = paginator.page_range
        if paginator.num_pages > 15:
            page_range = list(paginator.page_range[max(0, page_number - 7): page_number])
            page_range.extend(paginator.page_range[page_number: min(page_number + 7, paginator.num_pages)])
        return render(request, 'management/website/website_list.html', {'website_list': page_obj, 'page_range': page_range})


@method_decorator(csrf_exempt, name='dispatch')
class WebsiteCreate(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        form = WebsiteForm()
        if pk:
            website = Website.objects.get(id=pk)
            form = WebsiteForm(instance=website)
        return render(request, 'management/website/website_form.html', {'form': form})

    def post(self, request, pk=None):
        form = WebsiteForm(request.POST or None)
        if pk:
            instance = Website.objects.get(id=pk)
            form = WebsiteForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            url = reverse('management:website:index')
            if request.GET:
                url += '?' + request.GET.urlencode()
            return redirect(url)
        return render(request, 'management/website/website_form.html', {'form': form})


@login_required
@csrf_exempt
def website_remove(request, pk):
    url = reverse('management:website:index')
    if request.GET:
        url += '?' + request.GET.urlencode()
    if pk:
        website = Website.objects.get(pk=pk)
        # if operator.image:
        #     if os.path.exists(operator.image.path):
        #         os.remove(operator.image.path)
        # if operator.passport_scan:
        #     if os.path.exists(operator.passport_scan.path):
        #         os.remove(operator.passport_scan.path)
        website.delete()
    return redirect(url)
