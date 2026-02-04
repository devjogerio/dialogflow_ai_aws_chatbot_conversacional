# Usa uma imagem oficial leve do Python 3.10
# Slim é uma versão menor baseada em Debian, ideal para produção e dev por reduzir superfície de ataque e tamanho
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
# Todas as instruções subsequentes serão executadas a partir daqui
WORKDIR /app

# Define variáveis de ambiente para otimizar o Python no Docker
# PYTHONDONTWRITEBYTECODE 1: Evita a criação de arquivos .pyc (desnecessário em containers efêmeros)
# PYTHONUNBUFFERED 1: Garante que os logs sejam exibidos imediatamente no console (essencial para debug)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências do sistema necessárias para compilar pacotes Python e utilitários
# netcat-openbsd: Usado no entrypoint para verificar se o banco de dados está pronto (healthcheck de rede)
# gcc e libpq-dev: Necessários para compilar o adaptador psycopg2 do PostgreSQL
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requisitos para o container separadamente
# Isso aproveita o cache de camadas do Docker: se requirements.txt não mudar, o pip install não roda de novo
COPY requirements.txt .

# Instala as dependências do Python listadas no requirements.txt
# --upgrade pip garante a versão mais recente do gerenciador de pacotes
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o restante do código da aplicação para o diretório de trabalho
COPY . .

# Copia o script de ponto de entrada e dá permissão de execução
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Define o script de ponto de entrada que será executado ao iniciar o container
ENTRYPOINT ["/app/entrypoint.sh"]

# Comando padrão para iniciar o servidor Django
# 0.0.0.0:8000 expõe a aplicação para fora do container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
