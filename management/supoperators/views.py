from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from crm.forms import SupOperatorForm, OperatorFilterForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from crm.models import SupOperator
from django.urls import reverse
from django.views import View

UserModel = get_user_model()


@method_decorator(csrf_exempt, name='dispatch')
class SupOperatorList(LoginRequiredMixin, View):
    def get(self, request):
        filter_form = OperatorFilterForm(request.GET or None)
        sup_operators = SupOperator.objects.all().order_by('-created_at')
        if filter_form.is_valid():
            if filter_form.cleaned_data['name']:
                sup_operators = sup_operators.filter(name__icontains=filter_form.cleaned_data['name']).order_by('-created_at')
        paginator = Paginator(sup_operators, 20)
        page_number = int(request.GET.get('page', 1))
        page_obj = paginator.get_page(page_number)
        page_range = paginator.page_range
        if paginator.num_pages > 15:
            page_range = list(paginator.page_range[max(0, page_number - 7): page_number])
            page_range.extend(paginator.page_range[page_number: min(page_number + 7, paginator.num_pages)])
        return render(request, 'management/supoperator/supoperator_list.html', {'sup_operators': page_obj, 'page_range': page_range})


@method_decorator(csrf_exempt, name='dispatch')
class SupOperatorCreate(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        form = SupOperatorForm()
        if pk:
            sup_operator = SupOperator.objects.get(id=pk)
            form = SupOperatorForm(instance=sup_operator)
        return render(request, 'management/supoperator/supoperator_form.html', {'form': form})

    def post(self, request, pk=None):
        form = SupOperatorForm(request.POST or None, request.FILES or None)
        profile = None
        if pk:
            instance = SupOperator.objects.get(id=pk)
            profile = instance.profile
            form = SupOperatorForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            sup_operator = form.save(commit=False)
            if profile:
                profile.username = sup_operator.username
                profile.set_password(sup_operator.password)
                profile.save()
            else:
                profile = UserModel.objects.create_user(username=sup_operator.username, email=sup_operator.email, password=sup_operator.password, is_staff=True)
            sup_operator.profile = profile
            sup_operator.save()
            url = reverse('management:supoperator:index')
            if request.GET:
                url += '?' + request.GET.urlencode()
            return redirect(url)
        return render(request, 'management/supoperator/supoperator_form.html', {'form': form})


@login_required
@csrf_exempt
def sup_operator_remove(request, pk):
    url = reverse('management:supoperator:index')
    if request.GET:
        url += '?' + request.GET.urlencode()
    if pk:
        sup_operator = SupOperator.objects.get(pk=pk)
        # if operator.image:
        #     if os.path.exists(operator.image.path):
        #         os.remove(operator.image.path)
        # if operator.passport_scan:
        #     if os.path.exists(operator.passport_scan.path):
        #         os.remove(operator.passport_scan.path)
        profile = sup_operator.profile
        profile.delete()
    return redirect(url)
