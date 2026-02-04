#!/bin/bash

# ==============================================================================
# SCRIPT DE AUTOMAÇÃO DE DEPLOYMENT - NEXUS AI
# ==============================================================================
# Autor: Equipe DevOps Nexus
# Versão: 1.0.0
# Descrição: Automatiza o setup e execução do ambiente de desenvolvimento e produção.
# Suporta: Docker (Recomendado) e Instalação Local (Bare Metal).
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. CONFIGURAÇÕES VISUAIS E VARIÁVEIS GLOBAIS
# ------------------------------------------------------------------------------
# Cores para facilitar a leitura dos logs no terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Diretório raiz do projeto (assume que o script está em /scripts)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Arquivos de configuração
ENV_FILE="$PROJECT_ROOT/.env"
ENV_EXAMPLE="$PROJECT_ROOT/.env.example"

# ------------------------------------------------------------------------------
# 2. FUNÇÕES UTILITÁRIAS
# ------------------------------------------------------------------------------

# Função para imprimir logs formatados com timestamp
# Uso: log "INFO" "Mensagem"
log() {
    local type=$1
    local message=$2
    local color=$NC
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    case "$type" in
        "INFO") color=$BLUE ;;
        "SUCCESS") color=$GREEN ;;
        "WARN") color=$YELLOW ;;
        "ERROR") color=$RED ;;
    esac

    echo -e "${color}[$timestamp] [$type] $message${NC}"
}

# Função para verificar se um comando existe no sistema
# Encerra o script se uma dependência crítica estiver faltando
check_dependency() {
    if ! command -v "$1" &> /dev/null; then
        log "ERROR" "Dependência não encontrada: $1"
        log "WARN" "Por favor, instale $1 para continuar."
        exit 1
    else
        log "INFO" "Dependência verificada: $1"
    fi
}

# ------------------------------------------------------------------------------
# 3. PREPARAÇÃO DO AMBIENTE
# ------------------------------------------------------------------------------

# Configura as variáveis de ambiente
setup_env() {
    log "INFO" "Verificando configuração de ambiente..."
    
    if [ -f "$ENV_FILE" ]; then
        log "SUCCESS" "Arquivo .env encontrado."
    else
        log "WARN" "Arquivo .env não encontrado. Criando a partir do exemplo..."
        if [ -f "$ENV_EXAMPLE" ]; then
            cp "$ENV_EXAMPLE" "$ENV_FILE"
            log "SUCCESS" "Arquivo .env criado com sucesso."
            log "WARN" "⚠️  IMPORTANTE: Edite o arquivo .env com suas credenciais reais antes de prosseguir!"
            
            # Pausa para o usuário ler o aviso
            read -p "Pressione ENTER após confirmar as variáveis no .env..."
        else
            log "ERROR" "Arquivo .env.example não encontrado. Abortando."
            exit 1
        fi
    fi
}

# ------------------------------------------------------------------------------
# 4. ESTRATÉGIA: DOCKER (Recomendada)
# ------------------------------------------------------------------------------
run_docker() {
    log "INFO" "Iniciando processo de deploy via Docker..."

    # Verifica dependências do Docker
    check_dependency "docker"
    check_dependency "docker-compose"

    cd "$PROJECT_ROOT"

    log "INFO" "Parando containers antigos..."
    docker-compose down

    log "INFO" "Construindo imagens (Build)..."
    # --no-cache garante que pegamos as últimas versões das libs, útil em produção
    docker-compose build --no-cache

    log "INFO" "Iniciando serviços em background..."
    docker-compose up -d

    log "SUCCESS" "Ambiente Docker iniciado!"
    log "INFO" "Frontend: http://localhost:3000"
    log "INFO" "Backend: http://localhost:8000"
    log "INFO" "Use 'docker-compose logs -f' para acompanhar os logs."
}

# ------------------------------------------------------------------------------
# 5. ESTRATÉGIA: LOCAL (Desenvolvimento Avançado)
# ------------------------------------------------------------------------------
run_local() {
    log "INFO" "Iniciando setup do ambiente LOCAL..."

    # 5.1 Setup Backend (Python/Django)
    log "INFO" "Configurando Backend..."
    check_dependency "python3"
    
    cd "$PROJECT_ROOT/backend_core"
    
    # Cria virtualenv se não existir
    if [ ! -d "venv" ]; then
        log "INFO" "Criando ambiente virtual Python..."
        python3 -m venv venv
    fi

    # Ativa virtualenv
    source venv/bin/activate
    
    log "INFO" "Instalando dependências do Backend..."
    pip install -r requirements.txt
    
    log "INFO" "Aplicando migrações do banco de dados..."
    python manage.py migrate

    # 5.2 Setup Frontend (Node/Next.js)
    log "INFO" "Configurando Frontend..."
    check_dependency "npm"
    
    cd "$PROJECT_ROOT/frontend_client"
    
    log "INFO" "Instalando dependências do Frontend..."
    npm install

    log "SUCCESS" "Ambiente Local configurado com sucesso!"
    
    echo ""
    echo -e "${YELLOW}Para rodar a aplicação localmente, você precisará de 2 terminais:${NC}"
    echo -e "1. Backend: cd backend_core && source venv/bin/activate && python manage.py runserver"
    echo -e "2. Frontend: cd frontend_client && npm run dev"
    echo ""
}

# ------------------------------------------------------------------------------
# 6. MENU PRINCIPAL
# ------------------------------------------------------------------------------
show_menu() {
    clear
    echo -e "${BLUE}=========================================${NC}"
    echo -e "${BLUE}   NEXUS AI - FERRAMENTA DE DEPLOY       ${NC}"
    echo -e "${BLUE}=========================================${NC}"
    echo ""
    echo "Selecione o modo de operação:"
    echo "1) 🐳 Rodar via Docker (Recomendado)"
    echo "2) 💻 Setup de Ambiente Local"
    echo "3) 🧹 Limpar Ambientes (Docker Down & Clean)"
    echo "0) Sair"
    echo ""
    read -p "Opção: " option

    case $option in
        1)
            setup_env
            run_docker
            ;;
        2)
            setup_env
            run_local
            ;;
        3)
            cd "$PROJECT_ROOT"
            docker-compose down -v
            log "SUCCESS" "Ambiente limpo."
            ;;
        0)
            log "INFO" "Saindo..."
            exit 0
            ;;
        *)
            log "ERROR" "Opção inválida."
            sleep 1
            show_menu
            ;;
    esac
}

# Inicia o script chamando o menu
show_menu
