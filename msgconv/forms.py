from django import forms
    
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class SingleFileUploadForm(forms.Form):
    file = forms.FileField()
    executed = forms.TextInput()

class MultipleFileUploadForm(forms.Form):
    file = MultipleFileField()
    executed = forms.TextInput()
    
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': 'Name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'input',
        'placeholder': 'E-mail'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'textarea has-fixed-size',
        'placeholder': 'Your Message...',
        'cols': 30,
        'rows': 10
    }))