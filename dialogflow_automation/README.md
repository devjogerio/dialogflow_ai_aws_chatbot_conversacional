# Automação do Dialogflow ES

Este módulo fornece ferramentas para automatizar a criação e atualização de agentes, intenções e entidades no Dialogflow ES.

## Estrutura

- `config/`: Arquivos JSON de configuração (intenções, etc).
- `core/`: Lógica principal (Client, Parser, Logger).
- `main.py`: Ponto de entrada da CLI.

## Pré-requisitos

### Python

Recomenda-se o uso de **Python 3.9 a 3.12**.
⚠️ **Atenção**: Python 3.13+ (incluindo 3.14) pode apresentar incompatibilidades com a biblioteca `google-cloud-dialogflow` e `protobuf` (erro `Metaclasses with custom tp_new are not supported`).

### Instalação

1. Crie um ambiente virtual com uma versão estável do Python:

   ```bash
   # Exemplo usando o Python do sistema (macOS geralmente tem 3.9)
   /usr/bin/python3 -m venv venv
   source venv/bin/activate
   ```

2. Instale as dependências:

   ```bash
   pip install -r dialogflow_automation/requirements.txt
   ```

## Uso

Execute a ferramenta a partir da raiz do projeto:

```bash
python dialogflow_automation/main.py --help
```

### Exemplos

```bash
# Executar usando credenciais do .env
python dialogflow_automation/main.py

# Especificar credenciais manualmente
python dialogflow_automation/main.py --project-id meu-projeto --credentials chaves/minha-chave.json
```

## Solução de Problemas

- **ModuleNotFoundError: No module named 'dialogflow_automation'**:
  Certifique-se de executar o script a partir da **raiz do projeto** (`nexus_ai_aws_final`). O script `main.py` ajusta automaticamente o `PYTHONPATH`.

- **TypeError: Metaclasses with custom tp_new are not supported**:
  Você está usando uma versão muito recente do Python (ex: 3.14). Use uma versão estável (3.9 - 3.12).
