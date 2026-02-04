# Projeto Recriado: Nexus AI (AWS Edition) - Versão Final

Este documento descreve o processo completo de desenvolvimento, reestruturação e implementação final do projeto Nexus AI. O projeto foi recriado do zero no diretório `nexus_ai_aws_final` para garantir uma arquitetura limpa, modular e aderente às melhores práticas de Cloud e DevOps.

---

## 📂 Estrutura do Projeto Entregue

O projeto segue uma arquitetura de microsserviços e serverless, organizado em três módulos principais:

### 1. `backend_core/` (Django REST Framework)

- **Propósito:** Núcleo de gerenciamento de dados e regras de negócio.
- **Funcionalidades:**
  - API RESTful para gestão de **Tickets** e **Orçamentos**.
  - Endpoint de Chat (`/api/chat/`) integrado ao serviço RAG.
  - Modelagem de dados robusta com PostgreSQL.
- **Arquivos Chave:**
  - `models.py`: Definições de schema para banco de dados.
  - `rag_service.py`: Camada de serviço que abstrai a lógica de IA (Bedrock + OpenSearch).
  - `entrypoint.sh`: Script de inicialização resiliente para Docker.

### 2. `lambda_functions/` (AWS Lambda)

- **Propósito:** Webhook serverless para integração com Dialogflow.
- **Funcionalidades:**
  - Processamento de intenções de linguagem natural.
  - Roteamento inteligente entre fluxos de suporte técnico e comercial.
- **Arquivos Chave:**
  - `webhook_handler.py`: Lógica central do webhook com autenticação SigV4.

### 3. `frontend_client/` (Next.js + React)

- **Propósito:** Interface de usuário moderna e responsiva.
- **Funcionalidades:**
  - Chat em tempo real com feedback visual (loading states).
  - Integração direta com a API do Backend.
- **Arquivos Chave:**
  - `ChatWindow.tsx`: Componente principal do chat.
  - `src/app/`: Estrutura do Next.js App Router configurada com Tailwind CSS.

---

## 🐳 Infraestrutura & Dockerização

Implementamos uma configuração completa de containerização para garantir que o ambiente de desenvolvimento seja idêntico ao de produção (Paridade dev-prod).

### Orquestração (`docker-compose.yml`)

- **Serviços:**
  - `db`: PostgreSQL 15 (Persistência de dados).
  - `backend`: Django API (Python 3.10 Slim).
  - `frontend`: Next.js Client (Node 18 Alpine).
- **Rede:** `nexus_network` isolada para comunicação interna segura.
- **Volumes:** Mapeamento de código local para **Hot Reload** imediato.

### Dockerfiles Otimizados

- **Backend:** Uso de imagem `slim`, limpeza de caches e variáveis `PYTHONDONTWRITEBYTECODE`.
- **Frontend:** Uso de imagem `alpine` para reduzir tamanho final e superfície de ataque.

---

## ✅ Correções e Melhorias Realizadas

### 1. Frontend (Next.js)

- **Estrutura App Router:** Correção da árvore de diretórios (`src/app/layout.tsx`, `page.tsx`).
- **Configuração TypeScript:** Adição de `tsconfig.json` e tipos para evitar erros de linter.
- **Estilização:** Configuração completa do Tailwind CSS (`tailwind.config.ts`, `globals.css`).
- **Integração Real:** Substituição de mocks por chamadas `fetch` reais à API.

### 2. Backend (Django)

- **Módulo RAG:** Criação de `rag_service.py` para isolar a lógica de IA.
- **Endpoints:** Exposição da rota `/api/chat/` para consumo do frontend.
- **Dependências:** Atualização do `requirements.txt` com SDKs da AWS (`boto3`, `opensearch-py`).

---

## 🚀 Como Executar o Projeto

1. **Configurar Variáveis de Ambiente:**

   ```bash
   cp nexus_ai_aws_final/.env.example nexus_ai_aws_final/.env
   # Edite o .env com suas credenciais AWS se necessário
   ```

2. **Iniciar os Containers:**

   ```bash
   cd nexus_ai_aws_final
   docker-compose up --build
   ```

3. **Acessar a Aplicação:**
   - **Frontend:** [http://localhost:3000](http://localhost:3000)
   - **Backend API:** [http://localhost:8000](http://localhost:8000)
   - **Admin:** [http://localhost:8000/admin](http://localhost:8000/admin)

---

## 🔍 Relatório Técnico Final

O projeto atingiu um estado de **Release Candidate (v1.1.0)**. A arquitetura implementada segue rigorosamente os princípios do **12-Factor App**, com configurações externalizadas e serviços de apoio desacoplados.

A segurança foi priorizada através do uso de variáveis de ambiente para credenciais sensíveis e comunicação interna via rede Docker isolada. A escolha de tecnologias (Next.js, Django, PostgreSQL, AWS Bedrock) oferece um equilíbrio ideal entre produtividade de desenvolvimento e escalabilidade em produção.

### Próximos Passos Sugeridos

1. **Teste de Carga:** Simular múltiplos usuários simultâneos no Chat.
2. **Pipeline CI/CD:** Automatizar o deploy para AWS (ECS ou Lambda + Vercel).
3. **Monitoramento:** Configurar painéis no CloudWatch para logs do Backend e Lambda.
