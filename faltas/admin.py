from django.contrib import admin
from .models import Aluno, Menssagem


class lista_alunos(admin.ModelAdmin):
    list_display = ( "ra", "nome", "turma", "responsavel", "telefone")
    
    

class lista_mensagem(admin.ModelAdmin):    
    list_display = ( "nome_aluno", "falta_data", "msg_data", "msg_enviada")
    
    @admin.display(description="Aluno", ordering='aluno__nome')
    def nome_aluno(self, obj):
        return obj.aluno.nome
    

admin.site.register(Aluno, lista_alunos)
admin.site.register(Menssagem, lista_mensagem)
