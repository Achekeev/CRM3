from crm.models import DailyTotal, CamModel, Operator, Website, ProfileWebsite
from crm.forms import DailyTotalForm, AccountingFilterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q, Sum
from django.urls import reverse
from django.views import View


@method_decorator(csrf_exempt, name='dispatch')
class AccountingList(LoginRequiredMixin, View):
    def get(self, request):
        daily_totals = DailyTotal.objects.all().order_by('-created_at')
        filter_form = AccountingFilterForm(request.GET or None)
        date_from = request.GET.get('date_from', (datetime.today() - timedelta(days=datetime.today().weekday())).date().strftime('%Y-%m-%d'))
        date_to = request.GET.get('date_to', datetime.today().date().strftime('%Y-%m-%d'))
        if 'prev_week' in request.GET:
            if date_from is not None:
                prev_monday = datetime.strptime(date_from, '%Y-%m-%d') - timedelta(days=1)
                prev_monday = prev_monday - timedelta(days=prev_monday.weekday())
                prev_sunday = prev_monday + timedelta(days=6)
                date_from = prev_monday.strftime('%Y-%m-%d')
                date_to = prev_sunday.strftime('%Y-%m-%d')
            else:
                prev_monday = datetime.today() - timedelta(days=1)
                prev_monday = (prev_monday - timedelta(days=datetime.today().weekday())).date()
                date_from = prev_monday.strftime('%Y-%m-%d')
        if 'next_week' in request.GET:
            if date_from is not None:
                next_monday = datetime.strptime(date_from, '%Y-%m-%d') + timedelta(days=1)
                next_monday = next_monday + timedelta(days=7 - next_monday.weekday())
                next_sunday = next_monday + timedelta(days=6)
                date_from = next_monday.strftime('%Y-%m-%d')
                date_to = next_sunday.strftime('%Y-%m-%d')
        if filter_form.is_valid():
            if filter_form.cleaned_data['name']:
                daily_totals = daily_totals.filter(Q(cammodel_name__icontains=filter_form.cleaned_data['name']) | Q(operator_name__icontains=filter_form.cleaned_data['name'])).order_by('-created_at')
            if filter_form.cleaned_data['website']:
                daily_totals = daily_totals.filter(website_id=filter_form.cleaned_data['website'].id).order_by('-created_at')
        if date_from is not None:
            daily_totals = daily_totals.filter(created_at__date__gte=datetime.strptime(date_from, '%Y-%m-%d')).order_by('-created_at')
        if date_to is not None:
            daily_totals = daily_totals.filter(created_at__date__lte=datetime.strptime(date_to, '%Y-%m-%d')).order_by('-created_at')
        total = daily_totals.aggregate(Sum('total'))['total__sum']
        cammodel_total = daily_totals.aggregate(Sum('cammodel_amount'))['cammodel_amount__sum']
        operator_total = daily_totals.aggregate(Sum('operator_amount'))['operator_amount__sum']
        paginator = Paginator(daily_totals, 20)
        page_number = int(request.GET.get('page', 1))
        page_obj = paginator.get_page(page_number)
        page_range = paginator.page_range
        if paginator.num_pages > 15:
            page_range = list(paginator.page_range[max(0, page_number - 7): page_number])
            page_range.extend(paginator.page_range[page_number: min(page_number + 7, paginator.num_pages)])
        return render(request, 'management/accounting/accounting_list.html', locals())


@method_decorator(csrf_exempt, name='dispatch')
class AccountingCamModelStatistics(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        if pk:
            cammodel = CamModel.objects.get(id=pk)
            cammodel_dict = {'cammodel_id': cammodel.id, 'cammodel_name': cammodel.name, 'amount': 0, 'total': 0, 'websites': []}
            date_from = request.GET.get('date_from', (datetime.today() - timedelta(days=datetime.today().weekday())).date().strftime('%Y-%m-%d'))
            date_to = request.GET.get('date_to', datetime.today().date().strftime('%Y-%m-%d'))
            filter_form = AccountingFilterForm(request.GET or None)
            daily_totals = DailyTotal.objects.filter(cammodel_id=cammodel.id)
            if 'prev_week' in request.GET:
                if date_from is not None:
                    prev_monday = datetime.strptime(date_from, '%Y-%m-%d') - timedelta(days=1)
                    prev_monday = prev_monday - timedelta(days=prev_monday.weekday())
                    prev_sunday = prev_monday + timedelta(days=6)
                    date_from = prev_monday.strftime('%Y-%m-%d')
                    date_to = prev_sunday.strftime('%Y-%m-%d')
                else:
                    prev_monday = datetime.today() - timedelta(days=1)
                    prev_monday = (prev_monday - timedelta(days=datetime.today().weekday())).date()
                    date_from = prev_monday.strftime('%Y-%m-%d')
            if 'next_week' in request.GET:
                if date_from is not None:
                    next_monday = datetime.strptime(date_from, '%Y-%m-%d') + timedelta(days=1)
                    next_monday = next_monday + timedelta(days=7 - next_monday.weekday())
                    next_sunday = next_monday + timedelta(days=6)
                    date_from = next_monday.strftime('%Y-%m-%d')
                    date_to = next_sunday.strftime('%Y-%m-%d')
            if filter_form.is_valid():
                if filter_form.cleaned_data['website']:
                    daily_totals = daily_totals.filter(website_id=filter_form.cleaned_data['website'].id)
            if date_from is not None:
                daily_totals = daily_totals.filter(created_at__date__gte=datetime.strptime(date_from, '%Y-%m-%d')).order_by('-created_at')
            if date_to is not None:
                daily_totals = daily_totals.filter(created_at__date__lte=datetime.strptime(date_to, '%Y-%m-%d')).order_by('-created_at')
            data_list = []
            for website in cammodel.websites.all():
                website_dict = {'id': website.website.id, 'name': website.website.name, 'total': 0}
                cammodel_dict['websites'].append(website_dict)
            for total in daily_totals:
                cammodel_dict['total'] += total.total
                cammodel_dict['amount'] += total.cammodel_amount
                for website in cammodel_dict['websites']:
                    if website['id'] == total.website_id:
                        website['total'] += total.cammodel_amount
                        break
                for data in data_list:
                    if data['operator_id'] == total.operator_id:
                        data['total'] += total.total
                        data['amount'] += total.operator_amount
                        break
                else:
                    if total.operator_id:
                        new_dict = {'operator_id': total.operator_id, 'operator_name': total.operator_name, 'total': total.total, 'amount': total.operator_amount}
                        data_list.append(new_dict)
            return render(request, 'management/accounting/accounting_cammodel_statistics.html', locals())
        else:
            return redirect('management:cammodel:index')


@method_decorator(csrf_exempt, name='dispatch')
class AccountingOperatorStatistics(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        if pk:
            operator = Operator.objects.get(id=pk)
            operator_dict = {'operator_id': operator.id, 'operator_name': operator.name, 'amount': 0, 'total': 0, 'websites': []}
            date_from = request.GET.get('date_from', (datetime.today() - timedelta(days=datetime.today().weekday())).date().strftime('%Y-%m-%d'))
            date_to = request.GET.get('date_to', datetime.today().date().strftime('%Y-%m-%d'))
            filter_form = AccountingFilterForm(request.GET or None)
            daily_totals = DailyTotal.objects.filter(operator_id=operator.id)
            if 'prev_week' in request.GET:
                if date_from is not None:
                    prev_monday = datetime.strptime(date_from, '%Y-%m-%d') - timedelta(days=1)
                    prev_monday = prev_monday - timedelta(days=prev_monday.weekday())
                    prev_sunday = prev_monday + timedelta(days=6)
                    date_from = prev_monday.strftime('%Y-%m-%d')
                    date_to = prev_sunday.strftime('%Y-%m-%d')
                else:
                    prev_monday = datetime.today() - timedelta(days=1)
                    prev_monday = (prev_monday - timedelta(days=datetime.today().weekday())).date()
                    date_from = prev_monday.strftime('%Y-%m-%d')
            if 'next_week' in request.GET:
                if date_from is not None:
                    next_monday = datetime.strptime(date_from, '%Y-%m-%d') + timedelta(days=1)
                    next_monday = next_monday + timedelta(days=7 - next_monday.weekday())
                    next_sunday = next_monday + timedelta(days=6)
                    date_from = next_monday.strftime('%Y-%m-%d')
                    date_to = next_sunday.strftime('%Y-%m-%d')
            if filter_form.is_valid():
                if filter_form.cleaned_data['website']:
                    daily_totals = daily_totals.filter(website_id=filter_form.cleaned_data['website'].id)
            if date_from is not None:
                daily_totals = daily_totals.filter(created_at__date__gte=datetime.strptime(date_from, '%Y-%m-%d')).order_by('-created_at')
            if date_to is not None:
                daily_totals = daily_totals.filter(created_at__date__lte=datetime.strptime(date_to, '%Y-%m-%d')).order_by('-created_at')
            data_list = []
            for website in operator.websites.all():
                website_dict = {'id': website.website.id, 'name': website.website.name, 'total': 0}
                operator_dict['websites'].append(website_dict)
            for total in daily_totals:
                operator_dict['amount'] += total.operator_amount
                operator_dict['total'] += total.total
                for website in operator_dict['websites']:
                    if website['id'] == total.website_id:
                        website['total'] += total.operator_amount
                        break
            for total in daily_totals:
                for data in data_list:
                    if data['cammodel_id'] == total.cammodel_id:
                        data['amount'] += total.cammodel_amount
                        data['total'] += total.total
                        break
                else:
                    if total.cammodel_id:
                        new_dict = {'cammodel_id': total.cammodel_id, 'cammodel_name': total.cammodel_name, 'amount': total.cammodel_amount, 'total': total.total}
                        data_list.append(new_dict)
            return render(request, 'management/accounting/accounting_operator_statistics.html', locals())
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
        if pk:
            cammodel = CamModel.objects.get(id=pk)
            form.fields['website'].queryset = Website.objects.filter(id__in=cammodel.websites.values('website__id'))
            return render(request, 'management/accounting/accounting_form.html', {'form': form, 'cammodel': cammodel})
        messages.error(request, f'Произошла ошибка. {form.errors}')
        return HttpResponse(status=404)

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
            if form.cleaned_data['website']:
                instance.website_id = form.cleaned_data['website'].id
                instance.website_name = form.cleaned_data['website'].name
            try:
                if cammodel.operator:
                    instance.operator_id = cammodel.operator.id
                    instance.operator_name = cammodel.operator.name
                    if form.cleaned_data['website'] and not cammodel.operator.websites.filter(website__id=form.cleaned_data['website'].id).exists():
                        site = ProfileWebsite.objects.create(website=form.cleaned_data['website'])
                        cammodel.operator.websites.add(site)
            except Exception as e:
                pass
                # Who cares !?!
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
            operator = Operator.objects.get(id=pk)
            cammodel = operator.cammodel
        else:
            messages.error(request, f'Произошла ошибка. {form.errors}')
            return render(request, 'management/accounting/accounting_form.html', {'form': form})
        if form.is_valid():
            instance = form.save(commit=False)
            instance.cammodel_id = cammodel.id
            instance.cammodel_name = cammodel.name
            instance.operator_id = operator.id
            instance.operator_name = operator.name
            instance.calculate_rate()
            instance.save()
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
