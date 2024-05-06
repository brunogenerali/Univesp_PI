from django.shortcuts import render, redirect
from .models import DadosExcel, Aluno
from .forms import UploadForm, AddAlunos
import pandas as pd
from django.http import HttpResponse

# Create your views here.


def index(request):
    return render(request, 'faltas/index.html')


def processar_upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = request.FILES['arquivo']
            data = form.cleaned_data['data']
            try:
                df = pd.read_excel(arquivo, skiprows=13)
                dia = data.day  # Dia selecionado no formulário
                data_msg = str(f'{data.day}/{data.month}/{data.year}')
                # Filtrar os dados para o dia especificado
                df_filtrado = df[df[dia] > 4]
                df_novo = df_filtrado[['Aluno', 'RA', dia]]
                dados_list = []
                for index, row in df_novo.iterrows():
                    responsavel = Aluno.objects.get(
                        ra__exact=row['RA']).responsavel
                    telefone = Aluno.objects.get(ra__exact=row['RA']).telefone
                    mensagem = str(f'A PEI E. E. Antonio Marinho de Carvalho Filho, informa que o(a) aluno(a), {row['Aluno']}, está faltando hoje , {data_msg}, . No caso da razão da falta gerar atestado, aconselhamos trazer uma cópia para a escola, para justificar a falta do aluno. Obs: Os casos de excesso de faltas não justificadas serão encaminhados para o Conselho Tutelar. Caso o atestado já tenha sido entregue na escola, desconsidere a mensagem.')
                    dados = DadosExcel(
                        nome=row['Aluno'], documento=row['RA'], data=data, faltas=row[int(dia)], resp_aluno=responsavel, fone_aluno=telefone, mensagem_falta=mensagem)
                    dados.save()  # Salva os dados no banco de dados
                    dados_list.append(dados)

                return render(request, 'faltas/resultado.html', {
                    'dados': dados_list                    
                })

            except Exception as e:
                # Em caso de exceção, renderize o template de erro com a mensagem de erro e os dados coletados
                df_return = dados_list
                return render(request, 'faltas/erro.html', {
                    'mensagem': 'Mensagem de Erro ' + str(e),
                    'data': data,
                    'dia': dia,
                    'Responsavel': responsavel,
                    'df_return': df_return
                })

    else:
        form = UploadForm()
    return render(request, 'faltas/upload.html', {'form': form})


def add_alunos(request):
    if request.method == 'POST':
        form = AddAlunos(request.POST, request.FILES)
        if form.is_valid():
            arquivo = request.FILES['arquivo']
            try:
                df = pd.read_excel(arquivo)
                for index, row in df.iterrows():
                    aluno = Aluno(
                        nome=row['Aluno'],
                        ra=row['RA'],
                        turma=row['Turma'],
                        responsavel=row['Responsavel'],
                        telefone=row['Telefone']
                    )
                    aluno.save()
                return render(request, 'faltas/index.html')
            except Exception as e:
                return render(request, 'faltas/erro.html', {
                    'mensagem': 'Mensagem de Erro ' + str(e)})

    else:
        form = AddAlunos()
    return render(request, 'faltas/cadastro.html', {'form': form})

def upload(request):
    return HttpResponse("PAGINA UPLOAD")