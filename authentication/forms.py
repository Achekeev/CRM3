from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

UserModel = get_user_model()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')


class ProfileCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email',)
