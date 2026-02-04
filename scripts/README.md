# 🚀 Automação de Deployment - Nexus AI

Este diretório contém scripts utilitários para facilitar o ciclo de vida de desenvolvimento, teste e deployment da aplicação Nexus AI. O foco principal é padronizar a configuração de ambiente para reduzir o tempo de onboarding de novos desenvolvedores e garantir paridade entre desenvolvimento e produção.

## 🛠️ Ferramenta Principal: `deploy.sh`

O script `deploy.sh` é o orquestrador central para rodar o projeto. Ele abstrai comandos complexos do Docker e setup manual.

### Pré-requisitos

Para utilizar os scripts de automação, certifique-se de ter instalado:

- **Git** (Versionamento)
- **Docker & Docker Compose** (Para execução containerizada - Recomendado)
- **Python 3.10+** (Apenas para execução local)
- **Node.js 18+ & NPM** (Apenas para execução local)

### 📖 Como Usar

1. **Navegue até a raiz do projeto:**
   ```bash
   cd nexus_ai_aws_final
   ```

2. **Dê permissão de execução ao script:**
   ```bash
   chmod +x scripts/deploy.sh
   ```

3. **Execute o script:**
   ```bash
   ./scripts/deploy.sh
   ```

### ⚙️ Opções Disponíveis

Ao executar o script, um menu interativo será exibido com as seguintes opções:

#### 1) 🐳 Rodar via Docker (Recomendado)
Esta é a opção padrão para a maioria dos desenvolvedores.
- Verifica e cria o arquivo `.env` automaticamente.
- Para containers antigos para evitar conflitos de porta.
- Reconstrói as imagens (`build`) garantindo código atualizado.
- Inicia os serviços (Postgres, Django, Next.js) em modo `detached`.

#### 2) 💻 Setup de Ambiente Local
Utilize esta opção se precisar debugar código nativamente ou se não puder usar Docker.
- Cria um ambiente virtual Python (`venv`) isolado.
- Instala dependências do Backend (`pip install`).
- Executa migrações do banco de dados.
- Instala dependências do Frontend (`npm install`).
- **Nota:** Não inicia os servidores automaticamente; apenas prepara o ambiente.

#### 3) 🧹 Limpar Ambientes
- Remove containers, redes e volumes associados ao projeto (`docker-compose down -v`).
- Útil para resetar o banco de dados ou corrigir estados inconsistentes.

## 📝 Variáveis de Ambiente

O script verifica automaticamente a existência do arquivo `.env`. Se não existir, ele copia o `.env.example`.
**Atenção:** Você deve editar o arquivo `.env` gerado para incluir suas chaves reais da AWS (Bedrock, OpenSearch) e credenciais de banco de dados seguras.

## 🐛 Troubleshooting

**Erro: "Permission denied"**
Certifique-se de rodar `chmod +x scripts/deploy.sh`.

**Erro: "Docker daemon is not running"**
Abra o Docker Desktop antes de executar o script.

**Erro de Porta em uso (EADDRINUSE)**
Se as portas 3000 ou 8000 estiverem ocupadas, use a opção **3 (Limpar Ambientes)** ou encerre os processos manualmente.
