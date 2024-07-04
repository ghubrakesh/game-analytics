from django import forms

class UploadFileForm(forms.Form):
    file_ = forms.FileField(label='attach csv file')
