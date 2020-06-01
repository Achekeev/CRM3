from datetime import datetime

from crm.forms import DailyTotalForm, AccountingFilterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from crm.models import DailyTotal, CamModel, Operator
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from django.views import View


@method_decorator(csrf_exempt, name='dispatch')
class AccountingList(LoginRequiredMixin, View):
    def get(self, request):
        daily_totals = DailyTotal.objects.all().order_by('-created_at')
        filter_form = AccountingFilterForm(request.GET or None)
        if filter_form.is_valid():
            if filter_form.cleaned_data['name']:
                daily_totals = daily_totals.filter(Q(cammodel_name__icontains=filter_form.cleaned_data['name']) | Q(operator_name__icontains=filter_form.cleaned_data['name']))
            if filter_form.cleaned_data['date_from']:
                daily_totals = daily_totals.filter(created_at__date__gte=filter_form.cleaned_data['date_from'])
            if filter_form.cleaned_data['date_to']:
                daily_totals = daily_totals.filter(created_at__date__lte=filter_form.cleaned_data['date_to'])
        paginator = Paginator(daily_totals, 20)
        page_number = int(request.GET.get('page', 1))
        page_obj = paginator.get_page(page_number)
        page_range = paginator.page_range
        if paginator.num_pages > 15:
            page_range = list(paginator.page_range[max(0, page_number - 7): page_number])
            page_range.extend(paginator.page_range[page_number: min(page_number + 7, paginator.num_pages)])
        return render(request, 'management/accounting/accounting_list.html', {'daily_totals': page_obj, 'page_range': page_range, 'filter_form': filter_form})


@method_decorator(csrf_exempt, name='dispatch')
class AccountingCamModelStatistics(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        if pk:
            cammodel = CamModel.objects.get(id=pk)
            cammodel_dict = {'cammodel_id': cammodel.id, 'cammodel_name': cammodel.name, 'total': 0}
            filter_form = AccountingFilterForm(request.GET or None)
            daily_totals = DailyTotal.objects.filter(cammodel_id=cammodel.id)
            if filter_form.is_valid():
                if filter_form.cleaned_data['date_from']:
                    daily_totals = daily_totals.filter(created_at__date__gte=filter_form.cleaned_data['date_from'])
                if filter_form.cleaned_data['date_to']:
                    daily_totals = daily_totals.filter(created_at__date__lte=filter_form.cleaned_data['date_to'])
            data_list = []
            for total in daily_totals:
                cammodel_dict['total'] += total.cammodel_amount
            for total in daily_totals:
                for data in data_list:
                    if data['operator_id'] == total.operator_id:
                        data['total'] += total.operator_amount
                        break
                else:
                    if total.operator_id:
                        new_dict = {'operator_id': total.operator_id, 'operator_name': total.operator_name, 'total': total.operator_amount}
                        data_list.append(new_dict)
            return render(request, 'management/accounting/accounting_cammodel_statistics.html', {'data_list': data_list, 'cammodel_dict': cammodel_dict, 'filter_form': filter_form})
        else:
            return redirect('management:cammodel:index')

@method_decorator(csrf_exempt, name='dispatch')
class AccountingOperatorStatistics(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        if pk:
            operator = Operator.objects.get(id=pk)
            operator_dict = {'operator_id': operator.id, 'operator_name': operator.name, 'total': 0}
            filter_form = AccountingFilterForm(request.GET or None)
            daily_totals = DailyTotal.objects.filter(operator_id=operator.id)
            if filter_form.is_valid():
                if filter_form.cleaned_data['date_from']:
                    daily_totals = daily_totals.filter(created_at__date__gte=filter_form.cleaned_data['date_from'])
                if filter_form.cleaned_data['date_to']:
                    daily_totals = daily_totals.filter(created_at__date__lte=filter_form.cleaned_data['date_to'])
            data_list = []
            for total in daily_totals:
                operator_dict['total'] += total.operator_amount
            for total in daily_totals:
                for data in data_list:
                    if data['operator_id'] == total.operator_id:
                        data['total'] += total.operator_amount
                        break
                else:
                    if total.cammodel_id:
                        new_dict = {'cammodel_id': total.cammodel_id, 'cammodel_name': total.cammodel_name, 'total': total.cammodel_amount}
                        data_list.append(new_dict)
            return render(request, 'management/accounting/accounting_operator_statistics.html', {'data_list': data_list, 'operator_dict': operator_dict, 'filter_form': filter_form})
        else:
            return redirect('management:operator:index')


@method_decorator(csrf_exempt, name='dispatch')
class AccountingDetail(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        if pk:
            daily_total = DailyTotal.objects.get(id=pk)
            return render(request, 'management/accounting/accounting_detail.html', {'daily_total': daily_total})
        return HttpResponse(status=404)


@method_decorator(csrf_exempt, name='dispatch')
class AccountingCamModelForm(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        form = DailyTotalForm()
        cammodel = None
        if pk:
            cammodel = CamModel.objects.get(id=pk)
        return render(request, 'management/accounting/accounting_form.html', {'form': form, 'cammodel': cammodel})

    def post(self, request, pk=None):
        form = DailyTotalForm(request.POST or None)
        if pk:
            cammodel = CamModel.objects.get(id=pk)
        else:
            messages.error(request, f'Произошла ошибка. {form.errors}')
            return render(request, 'management/accounting/accounting_form.html', {'form': form})
        if form.is_valid():
            instance = form.save(commit=False)
            instance.cammodel_id = cammodel.id
            instance.cammodel_name = cammodel.name
            try:
                if cammodel.operator:
                    instance.operator_id = cammodel.operator.id
                    instance.operator_name = cammodel.operator.name
            except Exception as e:
                pass
            instance.calculate_rate()
            instance.save()
            url = reverse('management:accounting:index')
            if request.GET:
                url += '?' + request.GET.urlencode()
            return redirect(url)
        return render(request, 'management/accounting/accounting_form.html', {'form': form, 'cammodel': cammodel})


@method_decorator(csrf_exempt, name='dispatch')
class AccountingOperatorForm(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        form = DailyTotalForm()
        cammodel = None
        if pk:
            operator = Operator.objects.get(id=pk)
            cammodel = operator.cammodel
        if cammodel:
            return render(request, 'management/accounting/accounting_form.html', {'form': form, 'cammodel': cammodel})
        return HttpResponse(status=404)

    def post(self, request, pk=None):
        form = DailyTotalForm(request.POST or None)
        if pk:
            instance = DailyTotal.objects.get(id=pk)
            form = DailyTotalForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            url = reverse('management:accounting:index')
            if request.GET:
                url += '?' + request.GET.urlencode()
            return redirect(url)
        return render(request, 'management/accounting/accounting_form.html', {'form': form})


@login_required
@csrf_exempt
def daily_total_remove(request, pk):
    url = reverse('management:accounting:index')
    if request.GET:
        url += '?' + request.GET.urlencode()
    if pk:
        daily_total = DailyTotal.objects.get(pk=pk)
        # if operator.image:
        #     if os.path.exists(operator.image.path):
        #         os.remove(operator.image.path)
        # if operator.passport_scan:
        #     if os.path.exists(operator.passport_scan.path):
        #         os.remove(operator.passport_scan.path)
        daily_total.delete()
    return redirect(url)
