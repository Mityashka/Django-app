from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError


class USerBioForm(forms.Form):
    name = forms.CharField()
    age = forms.CharField(label='Your age', max_length=100, min_length=1)
    bio = forms.CharField(label="Biography", widget=forms.Textarea)

def validate_file_name(file: InMemoryUploadedFile):
    if file.name and 'virus' in file.name:
        raise ValidationError('File name cannot contain "virus"')

class UploadFilesForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name])
