from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from authapp.models import ShopUser, ShopUserProfile
from datetime import datetime, timedelta
import pytz
from django.conf import settings
import random, hashlib


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'avatar', 'email', 'age', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.is_active = False
        # salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        # user.activate_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.activate_key = hashlib.sha1(user.email.encode('utf8')).hexdigest()
        user.activate_key_expired = datetime.now(pytz.timezone(settings.TIME_ZONE))
        user.save()
        return user

    # def clean_age(self):
    #     data = self.cleaned_data['age']
    #     if data < 18 or data > 99:
    #         raise forms.ValidationError('Слишком молод!')
    #     return data
    #
    # def clean_email(self):
    #     data = self.cleaned_data['email']
    #     if ShopUser.objects.filter(email=data).exists():
    #         raise forms.ValidationError('Такой e-mail уже существует')
    #     return data


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'avatar', 'email', 'age', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    # def clean_age(self):
    #     data = self.cleaned_data['age']
    #     if data < 18 or data > 99:
    #         raise forms.ValidationError('Слишком молод!')
    #     return data
    #
    # def clean_email(self):
    #     data = self.cleaned_data['email']
    #     if ShopUser.objects.filter(email=data).exists():
    #         raise forms.ValidationError('Такой e-mail уже существует')
    #     return data


class ShopUserProfileEditForm(forms.ModelForm):
    class Meta:
        model = ShopUserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
