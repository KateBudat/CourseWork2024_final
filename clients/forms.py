from django import forms
from django.core.exceptions import ValidationError
from .models import Client
import re


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('first_name', 'second_name', 'gender', 'date_of_birth', 'telephone_number', 'note')
        labels = {
            'first_name': "Ім'я",
            'second_name': "Прізвище",
            'gender': "Стать",
            'date_of_birth': "День народження",
            'telephone_number': "Номер телефону",
            'note': "Нотатки",
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'second_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}, choices=(('', 'Оберіть стать'),
                                                                            ('чоловік', 'Чоловіча'),
                                                                            ('жінка', 'Жіноча'))),
            'date_of_birth': forms.DateInput(attrs={"type": "date", 'class': 'form-control'}),
            'telephone_number': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel',
                                                       'placeholder': 'хxx-xxx-xx-xx'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_telephone_number(self):
        telephone_number = self.cleaned_data['telephone_number']

        if not re.match(r'^0[0-9]{2}-[0-9]{3}-[0-9]{2}-[0-9]{2}$', telephone_number):
            raise ValidationError("Номер телефону повинен бути у форматі 'хxx-xxx-xx-xx'")
        return telephone_number

