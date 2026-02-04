from pathlib import Path
import os

# Caminho base do projeto (diretório pai do diretório onde este arquivo está)
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta para criptografia (Deve ser mantida segura em produção via variáveis de ambiente)
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 'django-insecure-default-key-change-in-prod')

# Modo de depuração (Não usar True em produção)
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Hosts permitidos para acessar a aplicação
ALLOWED_HOSTS = ['*']

# Configuração de CORS
CORS_ALLOW_ALL_ORIGINS = True  # Para desenvolvimento local, permite qualquer origem
# Para produção, especifique:
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
# ]

# Definição dos aplicativos instalados no projeto
INSTALLED_APPS = [
    'django.contrib.admin',          # Painel administrativo
    'django.contrib.auth',           # Sistema de autenticação
    'django.contrib.contenttypes',   # Framework de tipos de conteúdo
    'django.contrib.sessions',       # Gerenciamento de sessões
    'django.contrib.messages',       # Framework de mensagens
    'django.contrib.staticfiles',    # Arquivos estáticos (CSS, JS, Imagens)
    'rest_framework',                # Django REST Framework para criação de APIs
    'corsheaders',                   # CORS headers
    'tickets',                       # Nosso aplicativo customizado de Tickets
]

# Middlewares processam requisições e respostas globalmente
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # CORS Middleware (deve vir antes do CommonMiddleware)
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuração da URL principal de roteamento
ROOT_URLCONF = 'core.urls'

# Configuração de templates (HTML)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,  # Procura templates dentro das pastas dos apps
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Aplicação WSGI padrão para deploy
WSGI_APPLICATION = 'core.wsgi.application'

# Configuração do Banco de Dados
# Suporte híbrido: PostgreSQL (Docker/Prod) ou SQLite (Dev Local)
if os.environ.get('DB_ENGINE') == 'django.db.backends.postgresql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Validação de senhas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internacionalização
LANGUAGE_CODE = 'pt-br'  # Português do Brasil
TIME_ZONE = 'America/Sao_Paulo'  # Fuso horário
USE_I18N = True
USE_TZ = True

# Arquivos estáticos (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Configuração da chave primária padrão para modelos
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
