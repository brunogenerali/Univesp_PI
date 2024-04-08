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
    faltas_aluno = models.IntegerField(default=0)
    # falta_data = models.DateTimeField(auto_now=True, auto_now_add=False)
    msg_text = models.TextField()
    msg_data = models.DateTimeField(auto_now_add=True)


class DadosExcel(models.Model):
    nome = models.CharField(max_length=100)
    documento = models.CharField(max_length=20)
    data = models.DateField()
    faltas = models.IntegerField()
    resp_aluno = models.CharField(max_length=200, default='')
    fone_aluno = models.CharField(max_length=11, default=0)
