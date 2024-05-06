from django.contrib import admin
from .models import Aluno, Menssagem, DadosExcel

class lista_alunos(admin.ModelAdmin):
    list_display = ('nome','responsavel', 'telefone')

admin.site.register(Aluno, lista_alunos)
admin.site.register(Menssagem)
admin.site.register(DadosExcel)
