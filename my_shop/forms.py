from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'  # или перечислите только нужные поля

    def clean(self):
        cleaned_data = super().clean()
        try:
            product_sex = cleaned_data.get('sex')
            sex_list = cleaned_data.get('category').sex.all()
        except AttributeError:
            return cleaned_data

        if product_sex not in sex_list:
            self.add_error('sex', 'Для указанного пола категория не подходит.')

        return cleaned_data
