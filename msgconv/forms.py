from django import forms

class MyFileUploadForm(forms.Form):
    file = forms.FileField()
    