# Usando a imagem base python:3.4
FROM python

# Definindo variáveis de ambiente para o Django
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Atualizando os repositórios antes de instalar os pacotes
RUN apt-get update && apt-get upgrade -y

# Instalando dependências do sistema
RUN apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Criando e definindo o diretório de trabalho
WORKDIR /app

# Copiando o código da aplicação Django para o contêiner
COPY . /app/

# Instalando as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Coletando os arquivos estáticos
RUN python manage.py collectstatic --noinput
RUN python manage.py makemigrations
RUN python manage.py migrate

# Expondo a porta 9000 para acesso externo
EXPOSE 9000

# Comando para rodar o servidor WSGI com Gunicorn utilizando SSL
CMD ["gunicorn", "--workers=3", "setup.wsgi:application", "--bind", "0.0.0.0:9000"]

