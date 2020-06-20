from crm.forms import PairForm, CamModelFilterForm, PairWebsiteFormset
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from crm.models import Operator, ProfileWebsite
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Q
from django.views import View


@method_decorator(csrf_exempt, name='dispatch')
class PairList(LoginRequiredMixin, View):
    def get(self, request):
        filter_form = CamModelFilterForm(request.GET or None)
        pair_list = Operator.objects.filter(cammodel__isnull=False)
        if filter_form.is_valid():
            if filter_form.cleaned_data['name']:
                pair_list = pair_list.filter(Q(name__icontains=filter_form.cleaned_data['name']) | Q(cammodel__name__icontains=filter_form.cleaned_data['name'])).order_by('-created_at')
            if filter_form.cleaned_data['city']:
                pair_list = pair_list.filter(Q(city=filter_form.cleaned_data['city']) | Q(cammodel__city=filter_form.cleaned_data['city'])).order_by('-created_at')
            if filter_form.cleaned_data['website']:
                pair_list = pair_list.filter(Q(websites__website=filter_form.cleaned_data['website']) | Q(cammodel__websites__website=filter_form.cleaned_data['website'])).order_by('-created_at')
        paginator = Paginator(pair_list, 20)
        page_number = int(request.GET.get('page', 1))
        page_obj = paginator.get_page(page_number)
        page_range = paginator.page_range
        if paginator.num_pages > 15:
            page_range = list(paginator.page_range[max(0, page_number - 7): page_number])
            page_range.extend(paginator.page_range[page_number: min(page_number + 7, paginator.num_pages)])
        return render(request, 'management/pair/pair_list.html', {'pair_list': page_obj, 'page_range': page_range, 'filter_form': filter_form})


@method_decorator(csrf_exempt, name='dispatch')
class PairCreate(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        form = PairForm()
        website_formset = PairWebsiteFormset(queryset=ProfileWebsite.objects.none())
        if pk:
            operator = Operator.objects.get(id=pk)
            cammodel = operator.cammodel
            form = PairForm(initial={'operator': operator, 'cammodel': cammodel})
        return render(request, 'management/pair/pair_form.html', {'form': form, 'website_formset': website_formset})

    def post(self, request, pk=None):
        form = PairForm(request.POST or None)
        websites = PairWebsiteFormset(request.POST or None)
        if form.is_valid():
            operator = form.cleaned_data['operator']
            cammodel = form.cleaned_data['cammodel']
            operator.cammodel = cammodel
            operator.save()
            for website in websites:
                if website.is_valid():
                    if 'DELETE' in website.cleaned_data and website.cleaned_data['DELETE']:
                        if website.cleaned_data['id']:
                            website.cleaned_data['id'].delete()
                        continue
                    if website.empty_permitted and not website.has_changed():
                        continue
                    cammodel_website = website.save()
                    cammodel.websites.add(cammodel_website)
                    operator_website = ProfileWebsite.objects.create(website=website.cleaned_data['website'])
                    operator_website.url = website.cleaned_data['url']
                    operator_website.login = website.cleaned_data['operator_login']
                    operator_website.password = website.cleaned_data['operator_password']
                    operator_website.save()
                    operator.websites.add(operator_website)
            url = reverse('management:pair:index')
            if request.GET:
                url += '?' + request.GET.urlencode()
            return redirect(url)
        return render(request, 'management/pair/pair_form.html', {'form': form, 'website_formset': websites})


@login_required
@csrf_exempt
def pair_remove(request, pk):
    url = reverse('management:pair:index')
    if request.GET:
        url += '?' + request.GET.urlencode()
    if pk:
        operator = Operator.objects.get(pk=pk)
        operator.cammodel = None
        operator.save()
    return redirect(url)
