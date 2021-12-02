from authapp.forms import ShopUserEditForm, ShopUserProfileEditForm
from authapp.models import ShopUser, ShopUserProfile
from mainapp.models import ProductCategory, Product
from django import forms


class ShopUserAdminEdit(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'
        exclude = ('is_active',)


class ShopUserProfileEdit(ShopUserProfileEditForm):
    class Meta:
        model = ShopUserProfile
        fields = '__all__'
        exclude = ('is_active',)


class ProductCategoryEditForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'
        exclude = ('is_active',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('is_active',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProductCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'
        exclude = ('is_active',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
