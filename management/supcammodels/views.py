from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
import django.views.decorators.csrf
from crm.forms import SupModelForm
from django.urls import reverse
from crm.models import SupModel
from django.views import View

UserModel = get_user_model()


@method_decorator(django.views.decorators.csrf.csrf_exempt, name='dispatch')
class SupCamModelList(LoginRequiredMixin, View):
    def get(self, request):
        sup_cammodels = SupModel.objects.all().order_by('-created_at')
        paginator = Paginator(sup_cammodels, 20)
        page_number = int(request.GET.get('page', 1))
        page_obj = paginator.get_page(page_number)
        page_range = paginator.page_range
        if paginator.num_pages > 15:
            page_range = list(paginator.page_range[max(0, page_number - 7): page_number])
            page_range.extend(paginator.page_range[page_number: min(page_number + 7, paginator.num_pages)])
        return render(request, 'management/supcammodel/supcammodel_list.html', {'sup_cammodels': page_obj, 'page_range': page_range})


@method_decorator(django.views.decorators.csrf.csrf_exempt, name='dispatch')
class SupCamModelCreate(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        form = SupModelForm()
        if pk:
            sup_model = SupModel.objects.get(id=pk)
            form = SupModelForm(instance=sup_model)
        return render(request, 'management/supcammodel/supcammodel_form.html', {'form': form})

    def post(self, request, pk=None):
        form = SupModelForm(request.POST or None, request.FILES or None)
        profile = None
        if pk:
            instance = SupModel.objects.get(id=pk)
            profile = instance.profile
            form = SupModelForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            sup_operator = form.save(commit=False)
            if profile:
                profile.username = sup_operator.username
                profile.set_password(sup_operator.password)
                profile.save()
            else:
                profile = UserModel.objects.create_user(username=sup_operator.username, email=sup_operator.email, password=sup_operator.password)
            sup_operator.profile = profile
            sup_operator.save()
            url = reverse('management:supcammodel:index')
            if request.GET:
                url += '?' + request.GET.urlencode()
            return redirect(url)
        return render(request, 'management/supcammodel/supcammodel_form.html', {'form': form})


@login_required
@django.views.decorators.csrf.csrf_exempt
def sup_cammodel_remove(request, pk):
    url = reverse('management:supcammodel:index')
    if request.GET:
        url += '?' + request.GET.urlencode()
    if pk:
        sup_cammodel = SupModel.objects.get(pk=pk)
        # if operator.image:
        #     if os.path.exists(operator.image.path):
        #         os.remove(operator.image.path)
        # if operator.passport_scan:
        #     if os.path.exists(operator.passport_scan.path):
        #         os.remove(operator.passport_scan.path)
        profile = sup_cammodel.profile
        profile.delete()
    return redirect(url)
