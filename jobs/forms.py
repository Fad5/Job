# jobs/forms.py
from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }