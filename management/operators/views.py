from crm.forms import OperatorForm, OperatorFilterForm, ProfileWebsiteFormset
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from crm.models import Operator, ProfileWebsite
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.urls import reverse
from django.views import View


@method_decorator(csrf_exempt, name='dispatch')
class OperatorList(LoginRequiredMixin, View):
    def get(self, request):
        filter_form = OperatorFilterForm(request.GET or None)
        operators = Operator.objects.all().order_by('-created_at')
        if filter_form.is_valid():
            if filter_form.cleaned_data['name']:
                operators = operators.filter(name__icontains=filter_form.cleaned_data['name']).order_by('-created_at')
            if filter_form.cleaned_data['city']:
                operators = operators.filter(city=filter_form.cleaned_data['city']).order_by('-created_at')
            if filter_form.cleaned_data['website']:
                operators = operators.filter(websites__website=filter_form.cleaned_data['website']).order_by('-created_at')
        paginator = Paginator(operators, 20)
        page_number = int(request.GET.get('page', 1))
        page_obj = paginator.get_page(page_number)
        page_range = paginator.page_range
        if paginator.num_pages > 15:
            page_range = list(paginator.page_range[max(0, page_number - 7): page_number])
            page_range.extend(paginator.page_range[page_number: min(page_number + 7, paginator.num_pages)])
        return render(request, 'management/operator/operator_list.html', {'operators': page_obj, 'page_range': page_range, 'filter_form': filter_form})


@method_decorator(csrf_exempt, name='dispatch')
class OperatorDetail(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        if pk:
            operator = Operator.objects.get(id=pk)
            return render(request, 'management/operator/operator_detail.html', {'operator': operator})
        return HttpResponse(status=404)


@method_decorator(csrf_exempt, name='dispatch')
class OperatorCreate(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        form = OperatorForm()
        website_formset = ProfileWebsiteFormset(queryset=ProfileWebsite.objects.none())
        if pk:
            operator = Operator.objects.get(id=pk)
            form = OperatorForm(instance=operator)
            website_formset = ProfileWebsiteFormset(queryset=operator.websites.all())
        return render(request, 'management/operator/operator_form.html', {'form': form, 'website_formset': website_formset})

    def post(self, request, pk=None):
        form = OperatorForm(request.POST or None, request.FILES or None)
        websites = ProfileWebsiteFormset(request.POST or None)
        if pk:
            instance = Operator.objects.get(id=pk)
            form = OperatorForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            operator = form.save()
            for website in websites:
                if website.is_valid():
                    if 'DELETE' in website.cleaned_data and website.cleaned_data['DELETE']:
                        if website.cleaned_data['id']:
                            website.cleaned_data['id'].delete()
                        continue
                    if website.empty_permitted and not website.has_changed():
                        continue
                    website_instance = website.save()
                    operator.websites.add(website_instance)
            url = reverse('management:operator:index')
            if request.GET:
                url += '?' + request.GET.urlencode()
            return redirect(url)
        return render(request, 'management/operator/operator_form.html', {'form': form, 'website_formset': websites})


@login_required
@csrf_exempt
def operator_remove(request, pk):
    url = reverse('management:operator:index')
    if request.GET:
        url += '?' + request.GET.urlencode()
    if pk:
        operator = Operator.objects.get(pk=pk)
        # if operator.image:
        #     if os.path.exists(operator.image.path):
        #         os.remove(operator.image.path)
        # if operator.passport_scan:
        #     if os.path.exists(operator.passport_scan.path):
        #         os.remove(operator.passport_scan.path)
        operator.delete()
    return redirect(url)
