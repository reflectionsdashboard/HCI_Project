from django import forms
from .models import Topic, Reflection


class ReflectionForm(forms.ModelForm):
    class Meta:
        model = Reflection
        fields = ['id', 'description', 'subject', 'topic', 'accuracy', 'inaccuracy_category', 'comments']
        widgets = {
            'id': forms.HiddenInput(attrs={'readonly': 'true'}),
            'description': forms.HiddenInput(attrs={'readonly': 'true'}),
            'subject': forms.HiddenInput(attrs={'readonly': 'true'}),
            'topic': forms.Select(attrs={'class': 'custom-select my-1 mr-sm-2'}),
            'accuracy': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': '0'}),
            'inaccuracy_category': forms.Select(attrs={'class': 'custom-select my-1 mr-sm-2'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                              'placeholder': 'recommendations or comments'}),
        }

    def __init__(self, *args, **kwargs):
        super(ReflectionForm, self).__init__(*args, **kwargs)
        subject = self.initial.get('subject')
        self.fields['topic'].queryset = Topic.objects.filter(subject_id=subject)
