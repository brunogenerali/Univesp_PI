from django import forms

class UploadForm(forms.Form):
    arquivo = forms.FileField(label='Selecione o arquivo Excel')
    data = forms.DateField(label='Selecione a data', widget=forms.DateInput(attrs={'type': 'date'}))
