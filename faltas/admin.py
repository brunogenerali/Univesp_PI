from django.contrib import admin
from .models import Aluno, Menssagem, DadosExcel

admin.site.register(Aluno)
admin.site.register(Menssagem)
admin.site.register(DadosExcel)
