from django import forms
from django.core.exceptions import ValidationError
from users.models import Master
from datetime import date
import re


class MasterForm(forms.ModelForm):
    class Meta:
        model = Master
        fields = ('first_name', 'second_name', 'gender', 'telephone_number', 'specialization', 'hire_date')
        labels = {
            'first_name': "Ім'я",
            'second_name': "Прізвище",
            'gender': "Стать",
            'telephone_number': "Номер телефону",
            'specialization': "Спеціалізація",
            'hire_date': "Дата прийняття на роботу",
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'second_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}, choices=(('', 'Оберіть стать'), ('чоловік', 'Чоловіча'), ('жінка', 'Жіноча'))),
            'telephone_number': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel',
                                                       'placeholder': 'хxx-xxx-xx-xx'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_telephone_number(self):
        telephone_number = self.cleaned_data['telephone_number']
        if not re.match(r'^0[0-9]{2}-[0-9]{3}-[0-9]{2}-[0-9]{2}$', telephone_number):
            raise ValidationError("Номер телефону повинен бути у форматі 'хxx-xxx-xx-xx'")
        return telephone_number

    def clean_hire_date(self):
        hire_date = self.cleaned_data['hire_date']
        if hire_date < date.today():
            raise ValidationError("Дата прийняття на роботу повинна бути поточною або майбутньою")
        return hire_date
