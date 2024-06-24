# forms.py
from django import forms
from clients.models import Material, Supplier, Used_Material, Purchased_Material, Write_Off_Material


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ('name_material', 'brand', 'barcode')
        labels = {
            'name_material': "Назва матеріалу",
            'brand': "Бренд",
            'barcode': "Штрих-код",
        }
        widgets = {
            'name_material': forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px;'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px;'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px;'}),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['company_name', 'contact_person', 'contact_telephone']
        labels = {
            'company_name': 'Назва компанії',
            'contact_person': 'Контактна особа',
            'contact_telephone': 'Контактний телефон'
        }
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_telephone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UsedMaterialForm(forms.ModelForm):
    class Meta:
        model = Used_Material
        fields = ['used_amount']
        labels = {
            'used_amount': 'Використана кількість'
        }
        widgets = {
            'used_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class WriteOffMaterialForm(forms.ModelForm):
    class Meta:
        model = Write_Off_Material
        fields = ['amount', 'reason']
        labels = {
            'amount': 'Кількість',
            'reason': 'Причина',
        }
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'reason': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PurchasedMaterialForm(forms.ModelForm):
    class Meta:
        model = Purchased_Material
        fields = ['supplier', 'purchase_price', 'purchased_quantity', 'expiration_date']
        labels = {
            'supplier': 'Постачальник',
            'purchase_price': 'Ціна покупки',
            'purchased_quantity': 'Кількість',
            'expiration_date': 'Дата закінчення терміну',
        }
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'purchased_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


