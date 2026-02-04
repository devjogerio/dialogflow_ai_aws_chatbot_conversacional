# Nexus AI - Sistema Inteligente de Autoatendimento (AWS Edition)

Bem-vindo ao repositório oficial do **Nexus AI**, uma plataforma robusta de atendimento ao cliente impulsionada por IA Generativa na AWS. Este projeto utiliza uma arquitetura moderna e escalável para automatizar interações, gerenciar chamados e fornecer suporte técnico preciso.

---

## 📋 Visão Geral do Projeto

O Nexus AI foi projetado para reduzir a carga operacional de equipes de suporte (Nível 1), oferecendo respostas instantâneas e contextuais através de um chatbot inteligente.

### Principais Funcionalidades
1.  **Chatbot RAG (Retrieval-Augmented Generation):**
    *   Utiliza **AWS Bedrock (Claude v2)** para geração de respostas humanizadas.
    *   Consulta a base de conhecimento (manuais, PDFs) indexada no **Amazon OpenSearch**.
    *   Responde dúvidas técnicas com precisão, evitando alucinações.
2.  **Gestão Automatizada de Chamados:**
    *   Integração com **Dialogflow ES** para identificar intenções estruturadas.
    *   Abertura automática de tickets no backend **Django** quando o problema requer intervenção humana.
3.  **Geração de Orçamentos:**
    *   Cálculo dinâmico de propostas comerciais e simulação de envio de PDFs.
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

## 🚀 Guia de Instalação e Configuração

Siga os passos abaixo para configurar o ambiente de desenvolvimento.

### Pré-requisitos
*   Python 3.9+
*   Node.js 16+
*   Conta AWS ativa (com acesso a Bedrock, Lambda e OpenSearch)
*   Conta Google Cloud (para Dialogflow ES)

### 1. Configuração do Backend Core (Django)

Este módulo gerencia tickets, orçamentos e dados mestres.

```bash
# Navegue até a pasta do backend
cd nexus_ai_aws_final/backend_core

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Execute as migrações do banco de dados (SQLite por padrão)
python manage.py migrate

# Inicie o servidor de desenvolvimento
python manage.py runserver
# O backend estará rodando em http://localhost:8000
```

### 2. Configuração do Frontend (Next.js)

Interface de chat para o usuário final.

```bash
# Navegue até a pasta do frontend
cd nexus_ai_aws_final/frontend_client

# Instale as dependências
npm install

# Inicie o servidor de desenvolvimento
npm run dev
# Acesse o chat em http://localhost:3000
```

### 3. Configuração da AWS Lambda (Webhook)

O "cérebro" que conecta o Dialogflow aos serviços AWS.

1.  Acesse a pasta `nexus_ai_aws_final/lambda_functions`.
2.  Instale as dependências localmente para empacotamento:
    ```bash
    pip install -r requirements.txt -t .
    ```
3.  Crie um arquivo ZIP contendo todo o conteúdo da pasta.
4.  Faça o upload para uma nova função AWS Lambda (Runtime Python 3.9+).
5.  Configure as **Variáveis de Ambiente** no console da AWS:
    *   `BEDROCK_REGION`: Região do modelo (ex: `us-east-1`)
    *   `OPENSEARCH_HOST`: Endpoint do seu domínio OpenSearch
    *   `OPENSEARCH_INDEX`: Nome do índice (ex: `knowledge-base`)
    *   `DJANGO_API_URL`: URL pública do seu backend Django (use ngrok para testes locais)

---

## 📚 Documentação da API (Backend Core)

O backend expõe os seguintes endpoints REST:

*   **Tickets** (`/api/tickets/`)
    *   `GET`: Lista todos os chamados.
    *   `POST`: Cria um novo chamado (usado pelo Lambda).
    *   Payload exemplo:
        ```json
        {
          "customer_name": "João Silva",
          "problem_description": "Servidor não inicia",
          "status": "OPEN"
        }
        ```
*   **Orçamentos** (`/api/budgets/`)
    *   Gerenciamento de propostas geradas.

---

## 🧪 Testes e Validação

1.  **Teste de Unidade (Backend):** Execute `python manage.py test` no diretório `backend_core`.
2.  **Teste de Interface:** Abra o chat no navegador e envie "Tenho uma dúvida técnica".
3.  **Teste de Integração:** Verifique os logs do CloudWatch para garantir que o Lambda está invocando o Bedrock e o OpenSearch corretamente.

---

## 🤝 Contribuição

1.  Faça um Fork do projeto.
2.  Crie uma Branch para sua feature (`git checkout -b feature/MinhaFeature`).
3.  Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`).
4.  Push para a Branch (`git push origin feature/MinhaFeature`).
5.  Abra um Pull Request.

---

## 📄 Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

**Autores:** Equipe de Engenharia Nexus AI.
