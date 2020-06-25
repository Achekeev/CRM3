from crm.models import CamModel, SupModel, Operator, SupOperator, CamModelImage, CamModelRequest, CamModelRequestImage, DailyTotal, City, Website, ProfileWebsite
from django.forms import inlineformset_factory, modelformset_factory
from django import forms


class CamModelForm(forms.ModelForm):
    class Meta:
        model = CamModel
        exclude = ()


class CamModelImageForm(forms.ModelForm):
    class Meta:
        model = CamModelImage
        fields = ('image',)


CamModelImageFormset = inlineformset_factory(CamModel, CamModelImage, form=CamModelImageForm, can_delete=True, extra=1)


class ProfileWebsiteForm(forms.ModelForm):
    class Meta:
        model = ProfileWebsite
        exclude = ()


ProfileWebsiteFormset = modelformset_factory(ProfileWebsite, form=ProfileWebsiteForm, can_delete=True, extra=1)


class PairWebsiteForm(forms.ModelForm):
    operator_login = forms.CharField(label='Логин', max_length=255, required=False)
    operator_password = forms.CharField(label='Пароль', max_length=255, required=False)

    class Meta:
        model = ProfileWebsite
        exclude = ()


PairWebsiteFormset = modelformset_factory(ProfileWebsite, form=PairWebsiteForm, can_delete=True, extra=1)


class CamModelFilterForm(forms.Form):
    name = forms.CharField(label='По Имени', max_length=255, required=False, widget=forms.TextInput({'placeholder': 'Поиск По Имени'}))
    city = forms.ModelChoiceField(label='Город', queryset=City.objects.all(), required=False, empty_label='Поиск По Городу')
    website = forms.ModelChoiceField(label='Сайт', queryset=Website.objects.all(), required=False, empty_label='Поиск По Сайту')


class CamModelRequestForm(forms.ModelForm):
    schedule = forms.CharField(max_length=255, widget=forms.Textarea, required=False)
    login = forms.CharField(max_length=255, required=False)
    password = forms.CharField(max_length=255, required=False)

    class Meta:
        model = CamModelRequest
        exclude = ()


class CamModelRequestImageForm(forms.ModelForm):
    class Meta:
        model = CamModelRequestImage
        fields = ('image',)


CamModelRequestImageFormset = inlineformset_factory(CamModelRequest, CamModelRequestImage, form=CamModelRequestImageForm, can_delete=True, extra=1)


class SupModelForm(forms.ModelForm):
    class Meta:
        model = SupModel
        exclude = ('profile',)

    def __init__(self, *args, **kwargs):
        super(SupModelForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Должно быть уникальным'


class OperatorForm(forms.ModelForm):
    class Meta:
        model = Operator
        exclude = ()


class OperatorFilterForm(forms.Form):
    name = forms.CharField(label='По Имени', max_length=255, required=False, widget=forms.TextInput({'placeholder': 'Поиск По Имени'}))
    city = forms.ModelChoiceField(label='Город', queryset=City.objects.all(), required=False, empty_label='Поиск По Городу')
    website = forms.ModelChoiceField(label='Сайт', queryset=Website.objects.all(), required=False, empty_label='Поиск По Сайту')


class SupOperatorForm(forms.ModelForm):
    class Meta:
        model = SupOperator
        exclude = ('profile',)

    def __init__(self, *args, **kwargs):
        super(SupOperatorForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Должно быть уникальным'


class DailyTotalForm(forms.ModelForm):
    website = forms.ModelChoiceField(label='Сайт', queryset=Website.objects.all(), required=False, empty_label='Сайт')

    class Meta:
        model = DailyTotal
        fields = ('total',)


class AccountingFilterForm(forms.Form):
    name = forms.CharField(label='По Имени', max_length=255, required=False, widget=forms.TextInput({'placeholder': 'Поиск По Имени'}))
    date_from = forms.DateField(label='Дата с', required=False, widget=forms.TextInput({'placeholder': 'Дата с'}))
    date_to = forms.DateField(label='Дата по', required=False, widget=forms.TextInput({'placeholder': 'Дата по'}))
    website = forms.ModelChoiceField(label='Сайт', queryset=Website.objects.all(), required=False, empty_label='Выберите Сайт')


class PairForm(forms.Form):
    cammodel = forms.ModelChoiceField(label='Модель', queryset=CamModel.objects.all(), required=False)
    operator = forms.ModelChoiceField(label='Оператор', queryset=Operator.objects.all(), required=False)


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        exclude = ()


class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        exclude = ()
