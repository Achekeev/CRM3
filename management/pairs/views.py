from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from crm.models import Operator
from crm.forms import PairForm
from django.views import View


@method_decorator(csrf_exempt, name='dispatch')
class PairList(LoginRequiredMixin, View):
    def get(self, request):
        pair_list = Operator.objects.filter(cammodel__isnull=False)
        paginator = Paginator(pair_list, 20)
        page_number = int(request.GET.get('page', 1))
        page_obj = paginator.get_page(page_number)
        page_range = paginator.page_range
        if paginator.num_pages > 15:
            page_range = list(paginator.page_range[max(0, page_number - 7): page_number])
            page_range.extend(paginator.page_range[page_number: min(page_number + 7, paginator.num_pages)])
        return render(request, 'management/pair/pair_list.html', {'pair_list': page_obj, 'page_range': page_range})


@method_decorator(csrf_exempt, name='dispatch')
class PairCreate(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        form = PairForm()
        if pk:
            operator = Operator.objects.get(id=pk)
            cammodel = operator.cammodel
            form = PairForm(initial={'operator': operator, 'cammodel': cammodel})
        return render(request, 'management/pair/pair_form.html', {'form': form})

    def post(self, request, pk=None):
        form = PairForm(request.POST or None)
        if form.is_valid():
            operator = form.cleaned_data['operator']
            cammodel = form.cleaned_data['cammodel']
            operator.cammodel = cammodel
            operator.save()
            url = reverse('management:pair:index')
            if request.GET:
                url += '?' + request.GET.urlencode()
            return redirect(url)
        return render(request, 'management/pair/pair_form.html', {'form': form})


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
