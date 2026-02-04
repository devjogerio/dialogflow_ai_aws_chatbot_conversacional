# Roadmap de Versionamento - Nexus AI (AWS)

Este documento registra a evolução cronológica do projeto, destacando marcos importantes, novas funcionalidades e correções.

## [v1.1.1] - Governança e Versionamento
**Data de Lançamento:** 04 de Fevereiro de 2026
**Status:** Desenvolvimento
**Responsável:** Arquiteto de Software (Simulado)

### 🛡️ Governança de Código
- **Git Flow:** Implementação da estrutura de branches (`main`, `develop`, `feature/*`).
- **Padronização:** Configuração de `.gitignore` robusto para ignorar artefatos de build e arquivos sensíveis.
- **Code Review:** Criação de template de Pull Request (`.github/pull_request_template.md`) para garantir qualidade nas revisões.
- **Documentação:** Atualização do roadmap para refletir o ciclo de vida do desenvolvimento.

### 🔧 Ajustes Técnicos
- Configuração inicial do repositório Git.
- Definição de estratégia de commits semânticos (Conventional Commits).

---

## [v1.1.0] - Dockerização e Integração Completa
**Data de Lançamento:** 04 de Fevereiro de 2026
**Status:** Release Candidate (RC)

### 🐳 Infraestrutura & DevOps
- **Docker:** Implementação completa de containerização para ambiente local.
  - `Dockerfile` otimizado para Backend (Python Slim) e Frontend (Node Alpine).
  - `docker-compose.yml` orquestrando serviços (Django, Next.js, PostgreSQL).
  - `entrypoint.sh` com verificação de healthcheck do banco de dados.

### 🔗 Integração Backend-Frontend
- **API Real:** Substituição do Mock no Frontend por chamadas reais à API Django.
- **Endpoint de Chat:** Criação de `/api/chat/` no Django para processar mensagens RAG.
- **Serviço RAG:** Abstração da lógica de Bedrock e OpenSearch para `rag_service.py` reutilizável.

### 💅 Frontend Moderno
- **App Router:** Migração/Configuração para estrutura Next.js App Router (`src/app`).
- **Configuração:** Adição de `tsconfig.json` e `tailwind.config.ts` para suporte total a TypeScript e Estilização.

---

## [v1.0.0] - Versão Inicial Estável
**Data de Lançamento:** 04 de Fevereiro de 2026
**Status:** Produção (MVP)

### 🚀 Funcionalidades Lançadas
- **Core:**
  - Estrutura completa do projeto monorepo (`nexus_ai_aws_final`).
  - Backend Django configurado com API REST para Tickets e Orçamentos.
  - Modelagem de dados robusta (`models.py`) com validações.
- **IA & Serverless:**
  - Função AWS Lambda (`webhook_handler.py`) implementada e documentada.
  - Integração RAG funcional com OpenSearch e Bedrock (Claude).
  - Lógica de roteamento de intenções do Dialogflow.
- **Frontend:**
  - Componente de Chat (`ChatWindow.tsx`) com UX moderna.
  - Feedback visual de "digitando" e rolagem automática.

### 📝 Detalhamento Técnico
- **Backend:** Implementação dos ViewSets e Serializers para expor dados via JSON.
- **Segurança:** Adoção de variáveis de ambiente para credenciais sensíveis.
- **Qualidade de Código:** Adição de comentários explicativos linha a linha em todos os módulos principais.

---

## [v0.9.0] - Implementação do Frontend
**Timestamp:** 2026-02-04 15:45 UTC
- Criação do projeto Next.js.
- Desenvolvimento do componente `ChatWindow` com React Hooks (`useState`, `useEffect`).
- Implementação de chamadas assíncronas simuladas (Mock) para testes de UI.

---

## [v0.5.0] - Desenvolvimento do Webhook Serverless
**Timestamp:** 2026-02-04 14:30 UTC
- Escrita do script `webhook_handler.py`.
- Integração com SDKs da AWS (`boto3`, `opensearch-py`).
- Implementação da lógica de tratamento de erros e logs (CloudWatch).

---

## [v0.1.0] - Setup Inicial e Modelagem
**Timestamp:** 2026-02-04 12:00 UTC
- Criação da estrutura de diretórios.
- Definição dos modelos de dados (`Ticket`, `Budget`).
- Configuração inicial do Django (`settings.py`, `manage.py`).

---

## Próximos Passos (Roadmap v1.1.0)
- [ ] Implementar autenticação JWT no Frontend e Backend.
- [ ] Adicionar suporte a upload de arquivos no Chat (envio de prints de erro).
- [ ] Criar dashboard analítico para visualização de KPIs de atendimento.
- [ ] Automatizar deploy com Terraform (IaC).
