from crm.models import CamModel, SupModel, Operator, SupOperator, CamModelImage, CamModelRequest, CamModelRequestImage, DailyTotal
from django.forms import inlineformset_factory
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


class CamModelFilterForm(forms.Form):
    name = forms.CharField(label='По Имени', max_length=255, required=False, widget=forms.TextInput({'placeholder': 'Поиск По Имени'}))


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


class SupOperatorForm(forms.ModelForm):
    class Meta:
        model = SupOperator
        exclude = ('profile',)

    def __init__(self, *args, **kwargs):
        super(SupOperatorForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Должно быть уникальным'


class DailyTotalForm(forms.ModelForm):
    class Meta:
        model = DailyTotal
        fields = ('total',)


class AccountingFilterForm(forms.Form):
    name = forms.CharField(label='По Имени', max_length=255, required=False, widget=forms.TextInput({'placeholder': 'Поиск По Имени'}))
    date_from = forms.DateField(label='Дата с', required=False, widget=forms.TextInput({'placeholder': 'Дата с'}))
    date_to = forms.DateField(label='Дата по', required=False, widget=forms.TextInput({'placeholder': 'Дата по'}))
