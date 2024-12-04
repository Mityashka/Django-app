from django.contrib.auth.models import Group
from django import forms
from shopapp.models import Product
from django.forms import ModelForm

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'discount', 'preview']

    # images = forms.ImageField(
    #     widget=forms.ClearableFileInput(attrs={'multiple': True}),
    # )



class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name']

class CSVImportForm(forms.Form):
    csv_file = forms.FileField()
