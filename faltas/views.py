from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Aluno, Menssagem
from .forms import UploadForm, AddAlunos
import pandas as pd
from django.db import connection


def index(request):
    return render(request, "faltas/index.html")

def faltas_view(request):
    return render(request, "faltas/upload.html")

def sucesso_view(request):
    return render(request, "faltas/sucesso.html")


# Função para ler o Excel e retornar um DataFrame filtrado
def verificar_arquivo(arquivo, dia):
    try:
        df = pd.read_excel(arquivo, skiprows=13)
        df_filtrado = df[df[dia] > 4]  # Filtro básico de alunos com mais de 4 faltas
        df_novo = df_filtrado[["Aluno", "RA", dia]]
        return df_novo
    except Exception as e:
        raise Exception(f"Erro ao processar o Excel: {e}")


# Função para verificar se os alunos estão cadastrados
def verificar_alunos_cadastrados(df):
    alunos_faltantes = []

    for index, row in df.iterrows():
        try:
            Aluno.objects.get(ra=row["RA"])
        except Aluno.DoesNotExist:
            # Se não está cadastrado, adiciona à lista
            alunos_faltantes.append({"nome": row["Aluno"], "ra": row["RA"]})

    return alunos_faltantes


# View principal para processar o upload
def processar_upload(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = request.FILES["arquivo"]
            data = form.cleaned_data["data"]
            dia = data.day  # Obtém o dia da data selecionada
            data_msg = (
                f"{data.day}/{data.month}/{data.year}"  # Formata a data para a mensagem
            )

            try:
                # 1. Processa o Excel e gera o DataFrame
                df_novo = verificar_arquivo(arquivo, dia)

                # 2. Verifica se há alunos não cadastrados no banco de dados
                alunos_faltantes = verificar_alunos_cadastrados(df_novo)

                if alunos_faltantes:
                    # Se houver alunos faltantes, redireciona para a página de cadastro
                    return render(
                        request,
                        "faltas/cadastro_alunos.html",
                        {"alunos_faltantes": alunos_faltantes},
                    )

                # 3. Se todos os alunos estiverem cadastrados, gera as mensagens e salva os dados
                for index, row in df_novo.iterrows():
                    # Obtém o responsável e telefone do aluno no banco de dados
                    aluno = Aluno.objects.get(ra__exact=row["RA"])

                    # Verifica se já existe uma mensagem enviada para este aluno nesta data
                    if Menssagem.objects.filter(
                        aluno=aluno, falta_data=data, msg_enviada=True
                    ).exists():
                        # Se existir, pula para o próximo aluno
                        continue

                    # Gera a mensagem de falta
                    mensagem = (
                        f'A PEI E. E. Antonio Marinho de Carvalho Filho, informa que o(a) aluno(a), {row["Aluno"]}, está faltando hoje, {data_msg}. '
                        'No caso da razão da falta gerar atestado, aconselhamos trazer uma cópia para a escola, para justificar a falta do aluno. '
                        'Obs: Os casos de excesso de faltas não justificadas serão encaminhados para o Conselho Tutelar. Caso o atestado já tenha sido entregue na escola, desconsidere a mensagem.'
                    )

                    # Cria um novo registro no banco de dados
                    dados = Menssagem(
                        aluno=aluno,
                        faltas_aluno=row[int(dia)],
                        falta_data=data,
                        msg_text=mensagem,
                    )
                    dados.save()  # Salva os dados no banco de dados

                # 4. Filtra os dados para exibição
                dados_filtrados = Menssagem.objects.filter(
                    falta_data=data, msg_enviada=False
                ).select_related("aluno")

                # 5. Renderiza a página de resultado com os dados salvos
                return render(
                    request, "faltas/resultado.html", {"dados": dados_filtrados}
                )

            except Exception as e:
                return render(
                    request,
                    "faltas/erro.html",
                    {"mensagem": f"Mensagem de Erro: {str(e)}"},
                )

    else:
        form = UploadForm()

    return render(request, "faltas/upload.html", {"form": form})


def atualizar_msg_enviada(request, mensagem_id):
    if request.method == "POST":
        try:
            mensagem = Menssagem.objects.get(id=mensagem_id)
            mensagem.msg_enviada = True
            mensagem.save()
            return JsonResponse({"status": "success"})
        except Menssagem.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Mensagem não encontrada"}
            )
    return JsonResponse({"status": "error", "message": "Método inválido"})


def add_alunos(request):
    if request.method == "POST":
        form = AddAlunos(request.POST, request.FILES)
        if form.is_valid():
            arquivo = request.FILES["arquivo"]
            try:
                df = pd.read_excel(arquivo)
                for index, row in df.iterrows():
                    aluno = Aluno(
                        nome=row["Aluno"],
                        ra=row["RA"],
                        turma=row["Turma"],
                        responsavel=row["Responsavel"],
                        telefone=row["Telefone"],
                    )
                    aluno.save()
                return render(request, "faltas/cadastro_success.html")
            except Exception as e:
                return render(
                    request,
                    "faltas/erro.html",
                    {"mensagem": "Mensagem de Erro " + str(e)},
                )

    else:
        form = AddAlunos()
    return render(request, "faltas/cadastro.html", {"form": form})


def cadastrar_alunos(request):
    if request.method == "POST":
        print("POST data:", request.POST)

        # A quantidade de alunos enviados no formulário
        total_alunos = len(
            [key for key in request.POST.keys() if key.startswith("nome_")]
        )

        print(f"Total de alunos: {total_alunos}")  # Depuração: verificar quantos alunos estão sendo processados

        # Variável para rastrear se houve erro no cadastro
        erro_cadastro = False

        for i in range(1, total_alunos + 1):
            nome = request.POST[f"nome_{i}"]
            ra = request.POST[f"ra_{i}"]
            turma = request.POST[f"turma_{i}"]
            responsavel = request.POST[f"responsavel_{i}"]
            telefone = request.POST[f"telefone_{i}"]

            # Depuração: verificar se os dados estão corretos
            print(f"Cadastrando Aluno: {nome}, RA: {ra}, Turma: {turma}, Responsável: {responsavel}, Telefone: {telefone}")

            try:
                # Cadastra o aluno no banco de dados
                Aluno.objects.create(
                    nome=nome, ra=ra, turma=turma, responsavel=responsavel, telefone=telefone
                )
            except Exception as e:
                print(f"Erro ao cadastrar aluno {nome}: {e}")
                erro_cadastro = True  # Define que houve um erro no cadastro

        # Verifica se houve erro no cadastro
        if not erro_cadastro:
            # Redireciona para a página de resultados após o cadastro
            return redirect("sucesso")  # Substitua pelo nome da sua view de sucesso

        # Se houver erro, renderiza novamente com uma mensagem de erro, se desejado
        return render(
            request,
            "faltas/cadastro_alunos.html",
            {
                "alunos_faltantes": [],  # Passa uma lista vazia para evitar erro
                "error_message": "Houve um erro ao cadastrar alguns alunos. Tente novamente."  # Mensagem de erro
            },
        )

    # Se não for POST, redireciona ou trata o caso
    return render(
        request,
        "faltas/cadastro_alunos.html",
        {
            "alunos_faltantes": []  # Passa uma lista vazia para evitar erro
        },
    )


def confirm_clear_tables(request):
    return render(request, "faltas/confirm_clear_tables.html")


def clear_tables(request):
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM faltas_aluno")
            # cursor.execute("DELETE FROM faltas_dadosexcel")
        return render(request, "faltas/delete_success.html")
    return redirect("confirm_clear_tables")
