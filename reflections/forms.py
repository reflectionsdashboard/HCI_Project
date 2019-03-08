from django import forms
from . import models


class ReflectionForm(forms.ModelForm):
    class Meta:
        model = models.Reflection
        fields = ['id', 'description', 'subject', 'topic', 'accuracy', 'inaccuracy_category', 'comments']
        widgets = {
            'id': forms.HiddenInput(),
            'description': forms.HiddenInput(),
            'subject': forms.HiddenInput(),
            'topic': forms.Select(attrs={'class': 'custom-select my-1 mr-sm-2'}),
            'accuracy': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': '0'}),
            'inaccuracy_category': forms.Select(attrs={'class': 'custom-select my-1 mr-sm-2'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                              'placeholder': 'recommendations or comments'}),
        }
