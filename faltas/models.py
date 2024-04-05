from django.db import models

class Aluno(models.Model):
    ra = models.CharField(max_length=20)
    nome = models.CharField(max_length=200)
    turma = models.CharField(max_length=50)
    responsavel = models.CharField(max_length=200)
    telefone = models.CharField(max_length=11)
    ativo = models.BooleanField(default=True)
    
class Menssagem(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    msg_text = models.TextField()
    msg_data = models.DateTimeField()
    