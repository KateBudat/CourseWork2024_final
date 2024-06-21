from django import forms
from django.core.exceptions import ValidationError
from users.models import Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name_service', 'time_service', 'cost_service', 'percent_for_master', 'type_service']
        labels = {
            'name_service': "Назва",
            'time_service': "Тривалість",
            'cost_service': "Вартість",
            'percent_for_master': "Процент майстра",
            'type_service': "Тип послуги"
        }

        widgets = {
            'name_service': forms.TextInput(attrs={'class': 'form-control'}),
            'time_service': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost_service': forms.NumberInput(attrs={'class': 'form-control'}),
            'percent_for_master': forms.NumberInput(attrs={'class': 'form-control'}),
            'type_service': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_cost_service(self):
        cost_service = self.cleaned_data.get('cost_service')
        if cost_service is not None and cost_service < 0:
            raise ValidationError("Вартість не може бути від'ємною")
        return cost_service

    def clean_percent_for_master(self):
        percent_for_master = self.cleaned_data.get('percent_for_master')
        if percent_for_master is not None and (percent_for_master < 0 or percent_for_master > 100):
            raise ValidationError("Процент майстра повинен бути в межах від 0 до 100")
        return percent_for_master
