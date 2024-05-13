from django import forms

class UploadForm(forms.Form):
    arquivo = forms.FileField(
        label='Selecione o arquivo Excel',
        widget=forms.FileInput(attrs={
            'class': 'form-control row'
        })
        )
    data = forms.DateField(
        label='Selecione a data',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control mb-6 row'
            }))

class AddAlunos(forms.Form):
    arquivo = forms.FileField(label='Selecione o arquivo Excel')