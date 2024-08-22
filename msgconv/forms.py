from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.urls import reverse
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible
import logging

logger = logging.getLogger(__name__)

    
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
    executed = forms.CharField(
        widget=forms.TextInput(),
        required=False  # This makes the field optional
    )
    
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)

    MAX_UPLOAD_SIZE = 15 * 1024 * 1024  # 15MB

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > self.MAX_UPLOAD_SIZE:
                size_mb = file.size / (1024 * 1024)
                logger.info(f'File size exceeded for file: {file.name}')
                features_url = reverse('subscription') 
                error_message = mark_safe(_(
                    f"File size exceeds the 3MB limit.<br>"
                    f"Your file is {size_mb:.2f}MB.<br>"
                    f'<a href="{features_url}" target="_blank">Enroll in starter-pack</a> to convert bigger files.'
                ))
                raise ValidationError(
                    error_message,
                    code='file_too_large',
                )
        return file

    def clean(self):
        cleaned_data = super().clean()
        if 'file' not in cleaned_data and 'file' not in self._errors:
            raise ValidationError(_("No file was submitted."), code='no_file')
        return cleaned_data

class MultipleFileUploadForm(forms.Form):
    file = MultipleFileField()
    executed = forms.TextInput()
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)
    
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
    
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)