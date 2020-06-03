from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from crm.forms import CityForm
from django.views import View
from crm.models import City


@method_decorator(csrf_exempt, name='dispatch')
class CityList(LoginRequiredMixin, View):
    def get(self, request):
        city_list = City.objects.all()
        paginator = Paginator(city_list, 20)
        page_number = int(request.GET.get('page', 1))
        page_obj = paginator.get_page(page_number)
        page_range = paginator.page_range
        if paginator.num_pages > 15:
            page_range = list(paginator.page_range[max(0, page_number - 7): page_number])
            page_range.extend(paginator.page_range[page_number: min(page_number + 7, paginator.num_pages)])
        return render(request, 'management/city/city_list.html', {'city_list': page_obj, 'page_range': page_range})


@method_decorator(csrf_exempt, name='dispatch')
class CityCreate(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        form = CityForm()
        if pk:
            city = City.objects.get(id=pk)
            form = CityForm(instance=city)
        return render(request, 'management/city/city_form.html', {'form': form})

    def post(self, request, pk=None):
        form = CityForm(request.POST or None)
        if pk:
            instance = City.objects.get(id=pk)
            form = CityForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            url = reverse('management:city:index')
            if request.GET:
                url += '?' + request.GET.urlencode()
            return redirect(url)
        return render(request, 'management/city/city_form.html', {'form': form})


@login_required
@csrf_exempt
def city_remove(request, pk):
    url = reverse('management:city:index')
    if request.GET:
        url += '?' + request.GET.urlencode()
    if pk:
        city = City.objects.get(pk=pk)
        # if operator.image:
        #     if os.path.exists(operator.image.path):
        #         os.remove(operator.image.path)
        # if operator.passport_scan:
        #     if os.path.exists(operator.passport_scan.path):
        #         os.remove(operator.passport_scan.path)
        city.delete()
    return redirect(url)
