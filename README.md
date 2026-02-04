# Nexus AI - Sistema Inteligente de Autoatendimento (AWS Edition)

Bem-vindo ao repositório oficial do **Nexus AI**, uma plataforma robusta de atendimento ao cliente impulsionada por IA Generativa na AWS e Dialogflow. Este projeto utiliza uma arquitetura moderna e escalável para automatizar interações, gerenciar chamados e fornecer suporte técnico preciso.

---

## 📋 Visão Geral do Projeto

O Nexus AI foi projetado para reduzir a carga operacional de equipes de suporte (Nível 1), oferecendo respostas instantâneas e contextuais através de um chatbot inteligente. A solução integra Dialogflow ES para reconhecimento de intenções e AWS Bedrock para geração de respostas complexas via RAG.

### Principais Funcionalidades

1.  **Automação de Dialogflow (Novo!):**
    *   **Infraestrutura como Código (IaC):** Gerenciamento de Intents e Entities via arquivos JSON.
    *   **Validação de Schema:** Garante que os arquivos de configuração estejam corretos antes da execução.
    *   **Idempotência:** Scripts inteligentes que criam ou atualizam recursos sem duplicidade.
    *   **Logs Detalhados:** Monitoramento completo das operações de sincronização.

2.  **Chatbot RAG (Retrieval-Augmented Generation):**
    *   Utiliza **AWS Bedrock (Claude v2)** para geração de respostas humanizadas.
    *   Consulta a base de conhecimento (manuais, PDFs) indexada no **Amazon OpenSearch**.
    *   Responde dúvidas técnicas com precisão, evitando alucinações.

3.  **Gestão Automatizada de Chamados:**
    *   Integração com **Dialogflow ES** para identificar intenções estruturadas.
    *   Abertura automática de tickets no backend **Django** quando o problema requer intervenção humana.

4.  **Interface de Usuário Moderna:**
    *   Frontend em **Next.js** com chat em tempo real e design responsivo.

---

## 🏗 Arquitetura Técnica

O sistema segue uma arquitetura híbrida serverless/microsserviços na AWS:

```mermaid
graph TD
    User[Usuário Final] -->|Interage| NextJS[Frontend Client (Next.js)]
    NextJS -->|API| Dialogflow[Dialogflow ES Agent]
    Dialogflow -->|Webhook| Lambda[AWS Lambda (Webhook Handler)]
    
    subgraph "AWS Cloud Ecosystem"
        Lambda -->|Busca Contexto| OpenSearch[Amazon OpenSearch (Vector DB)]
        Lambda -->|Gera Resposta| Bedrock[AWS Bedrock (Claude Model)]
        Lambda -->|Cria Ticket| DjangoAPI[Backend Core (Django REST)]
        
        OpenSearch -.->|Indexa| S3[Amazon S3 (Knowledge Base)]
    end
    
    DjangoAPI -->|Persiste Dados| RDS[Amazon RDS (PostgreSQL)]
```

---

## 📂 Estrutura do Projeto

```text
nexus_ai_aws_final/
├── backend_core/           # API Django para gestão de tickets e orçamentos
├── dialogflow_automation/  # Scripts de automação do Dialogflow (IaC)
│   ├── config/             # Configurações JSON (intents.json)
│   ├── core/               # Lógica principal (Client, Parser, Logger)
│   └── main.py             # Ponto de entrada do script de automação
├── frontend_client/        # Interface de Chat em Next.js (React)
├── lambda_functions/       # Webhooks AWS Lambda para integração
├── scripts/                # Scripts utilitários de deploy
├── tests/                  # Testes automatizados (Unitários e Integração)
└── .env.example            # Exemplo de variáveis de ambiente
```

---

## 🚀 Guia de Instalação e Configuração

Siga os passos abaixo para configurar o ambiente de desenvolvimento completo.

### Pré-requisitos
*   Python 3.9+ (Recomendado 3.10+)
*   Node.js 16+
*   Conta AWS ativa (Bedrock, Lambda, OpenSearch)
*   Conta Google Cloud (Dialogflow ES) e arquivo `credentials.json`

### 1. Configuração do Backend Core (Django)

Este módulo gerencia tickets, orçamentos e dados mestres.

```bash
# Navegue até a pasta do backend
cd backend_core

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Execute as migrações e inicie o servidor
python manage.py migrate
python manage.py runserver
```

### 2. Configuração do Frontend (Next.js)

Interface de chat para o usuário final.

```bash
cd frontend_client
npm install
npm run dev
# Acesse em http://localhost:3000
```

### 3. Automação do Dialogflow (IaC)

Este módulo permite sincronizar suas intenções e entidades definidas em JSON diretamente com o Dialogflow.

**Instalação:**

```bash
# Na raiz do projeto
python -m venv venv_stable
source venv_stable/bin/activate
pip install -r dialogflow_automation/requirements.txt
```

**Execução:**

```bash
# Sincronizar Intents e Entities
python dialogflow_automation/main.py --project-id SEU_PROJECT_ID --credentials credentials.json
```

**Arquivos de Configuração:**
*   Edite `dialogflow_automation/config/intents.json` para adicionar novas intenções. O script valida automaticamente o schema do JSON.

---

## 🧪 Testes e Validação

### Testes de Unidade (Automação)
O projeto inclui uma suite de testes para garantir a integridade da automação do Dialogflow.

```bash
# Execute na raiz do projeto
python -m unittest discover tests/dialogflow_automation
```

### Testes de Backend
```bash
cd backend_core
python manage.py test
```

---

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`. As principais variáveis são:

```env
# AWS Configuration
BEDROCK_REGION=us-east-1
OPENSEARCH_HOST=seu-endpoint.opensearch.amazonaws.com
OPENSEARCH_INDEX=knowledge-base

# Django Configuration
DJANGO_SECRET_KEY=sua-chave-secreta-segura
DEBUG=True

# Dialogflow Automation
GOOGLE_APPLICATION_CREDENTIALS=./credentials.json
DIALOGFLOW_PROJECT_ID=nexus-ai-aws-v1-ahuj
```

---

## 🤝 Contribuição

1.  Faça um Fork do projeto.
2.  Crie uma Branch para sua feature (`git checkout -b feature/MinhaFeature`).
3.  Commit suas mudanças (`git commit -m 'feat: Adiciona nova funcionalidade X'`).
4.  Push para a Branch (`git push origin feature/MinhaFeature`).
5.  Abra um Pull Request detalhando suas alterações.

---

## 📄 Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

**Autores:** Equipe de Engenharia Nexus AI.
