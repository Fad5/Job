# jobs/forms.py
from django import forms
from .models import Job, Response

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['message', 'proposed_price']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Расскажите, почему вы подходите для этого задания...'
            }),
            'proposed_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Можете предложить свою цену (необязательно)'
            }),
        }
        labels = {
            'message': 'Ваше сообщение',
            'proposed_price': 'Предложенная цена (руб.)',
        }