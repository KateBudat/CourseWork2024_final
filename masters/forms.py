from django import forms
from django.core.exceptions import ValidationError
from clients.models import Master
from datetime import date
import re


class MasterForm(forms.ModelForm):
    class Meta:
        model = Master
        fields = ('first_name', 'second_name', 'gender', 'telephone_number', 'specialization')
        labels = {
            'first_name': "Ім'я",
            'second_name': "Прізвище",
            'gender': "Стать",
            'telephone_number': "Номер телефону",
            'specialization': "Спеціалізація",
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'second_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}, choices=(('', 'Оберіть стать'), ('чоловік', 'Чоловіча'), ('жінка', 'Жіноча'))),
            'telephone_number': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel',
                                                       'placeholder': '0xx-xxx-xx-xx'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_telephone_number(self):
        telephone_number = self.cleaned_data['telephone_number']
        if not re.match(r'^0[0-9]{2}-[0-9]{3}-[0-9]{2}-[0-9]{2}$', telephone_number):
            raise ValidationError("Номер телефону повинен бути у форматі '0xx-xxx-xx-xx'")
        return telephone_number
