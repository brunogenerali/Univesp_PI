from django.shortcuts import render, redirect
from .models import DadosExcel, Aluno
from .forms import UploadForm
import pandas as pd

# Create your views here.

def index(request):
    return render(request, 'faltas/index.html')

# def processar_upload(request):
#     if request.method == 'POST':
#         form = UploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             arquivo = request.FILES['arquivo']
#             data = form.cleaned_data['data']
#             try:
#                 df = pd.read_excel(arquivo, skiprows=13)                
#                 dia = data.day  # Dia selecionado no formulário
#                 if str(dia) in df.columns:
#                     df_filtrado = df[df[str(dia)] > 4]  # Filtrar os dados para o dia especificado
#                     dados_list = []
#                     for index, row in df_filtrado.iterrows():
#                         dados = DadosExcel(nome=row['Aluno'], documento=row['RA'], data=data, faltas=row[str(dia)], processado_recentemente=True)
#                         dados_list.append(dados)
#                     DadosExcel.objects.bulk_create(dados_list)  # Salvar os dados no banco de dados
#                     #request.session['dados_processados'] = dados_list  # Salvar os dados na sessão
#                     #return redirect('resultado')
#                     df_erro = DadosExcel.objects.filter(data=data)                    
#                     return render(request, 'faltas/resultado.html', {'dados': dados_list})
#                 else:
#                     #df_html = df[df[int(dia)] > 4].to_html()
#                     df_html = dados_list
#                     return render(request, 'faltas/erro.html', {'mensagem': 'A coluna do dia especificado não existe no arquivo', 'colunas': dia, 'df_html': df_erro})            
#                     # return render(request, 'faltas/erro.html', {'mensagem': 'A coluna do dia especificado não existe no arquivo'})
#             except Exception as e:
#                 # Em caso de exceção, renderize o template de erro com a mensagem de erro e o DataFrame em HTML
#                 df_html = df.to_html()
#                 return render(request, 'faltas/erro.html', {'mensagem': 'Erro ao processar o arquivo: ' + str(e), 'colunas': dia, 'df_html': df_html})    
#                 # return render(request, 'faltas/erro.html', {'mensagem': 'Erro ao processar o arquivo: ' + str(e)})
#     else:
#         form = UploadForm()
#     return render(request, 'faltas/upload.html', {'form': form})

def processar_upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = request.FILES['arquivo']
            data = form.cleaned_data['data']            
            try:
                df = pd.read_excel(arquivo, skiprows=13)
                dia = data.day  # Dia selecionado no formulário
                df_filtrado = df[df[dia]>4]  # Filtrar os dados para o dia especificado
                df_novo = df_filtrado[['Aluno', 'RA', dia]]                
                dados_list = []                
                for index, row in df_novo.iterrows():
                    responsavel = Aluno.objects.get(ra__exact = row['RA']).responsavel
                    telefone = Aluno.objects.get(ra__exact = row['RA']).telefone
                    dados = DadosExcel(nome=row['Aluno'], documento=row['RA'], data=data, faltas=row[int(dia)])
                    dados.save() # Salva os dados no banco de dados                    
                    dados_list.extend(dados)
                    
                                    
                return render(request, 'faltas/resultado.html', {'dados': dados_list, 'Responsavel': responsavel})                
            except Exception as e:
                # Em caso de exceção, renderize o template de erro com a mensagem de erro e o DataFrame em HTML                
                df_return = dados_list
                return render(request, 'faltas/erro.html', {'mensagem': 'Mensagem de Erro ' + str(e),  'data': data, 'dia': dia, 'Responsavel': responsavel, 'df_return': df_return})
                
                
    else:
        form = UploadForm()
    return render(request, 'faltas/upload.html', {'form': form})

def add_alunos(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = request.FILES['arquivo']
            try:
                df = pd.read_excel(arquivo, skiprows=13)
                df_filtrado = df[['Aluno', 'RA']]
            except:
                pass
                
    else:
        form = UploadForm()
    return render(request, 'faltas/cadastro.html', {'form': form})