import json
import boto3
import os
import logging
import requests
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

# Configuração de Logs para monitoramento no CloudWatch
# O nível de log INFO é adequado para ambientes de produção.
# Cuidado: Logs DEBUG podem expor informações sensíveis (PII).
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# --- Configurações de Variáveis de Ambiente ---
# Utilizando variáveis de ambiente para manter a configuração separada do código (12-factor app).
# Isso permite implantar o mesmo código em diferentes ambientes (Dev, Staging, Prod) apenas alterando as variáveis.
BEDROCK_REGION = os.environ.get('BEDROCK_REGION', 'us-east-1')
OPENSEARCH_HOST = os.environ.get('OPENSEARCH_HOST')
OPENSEARCH_INDEX = os.environ.get('OPENSEARCH_INDEX', 'knowledge-base')
DJANGO_API_URL = os.environ.get('DJANGO_API_URL', 'http://localhost:8000/api') # URL base da API Django

# --- Inicialização de Clientes AWS ---
# Inicializa o cliente do AWS Bedrock Runtime.
# Este cliente é responsável por invocar os modelos de IA (Foundation Models) para inferência.
bedrock_client = boto3.client(service_name='bedrock-runtime', region_name=BEDROCK_REGION)

def get_opensearch_client():
    """
    Cria e retorna um cliente OpenSearch configurado com autenticação AWS (SigV4).
    A autenticação SigV4 é necessária para acessar domínios do OpenSearch protegidos por políticas IAM.
    """
    region = os.environ.get('AWS_REGION', 'us-east-1')
    service = 'es'
    credentials = boto3.Session().get_credentials()
    
    # AWS4Auth assina as requisições HTTP com as credenciais temporárias do Lambda (Role IAM)
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    # Criação do cliente OpenSearch de baixo nível
    client = OpenSearch(
        hosts=[{'host': OPENSEARCH_HOST, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    return client

def lambda_handler(event, context):
    """
    Função principal (Entry Point) do AWS Lambda para o Webhook do Dialogflow.
    Recebe eventos JSON do Dialogflow, processa a intenção detectada e retorna uma resposta formatada.
    """
    logger.info(f"Evento recebido: {json.dumps(event)}")

    try:
        # --- Parsing do Evento ---
        # Extrai o corpo da requisição, que contém os detalhes da conversa do Dialogflow
        body = json.loads(event['body'])
        query_result = body.get('queryResult', {})
        
        # Identifica a intenção (Intent) detectada pelo Dialogflow
        intent_name = query_result.get('intent', {}).get('displayName')
        
        # Extrai o texto original digitado pelo usuário
        user_query = query_result.get('queryText')
        
        # Extrai os parâmetros (entidades) capturados pelo Dialogflow
        parameters = query_result.get('parameters', {})

        response_text = "Desculpe, não entendi. Pode repetir?"

        # --- Roteamento de Intenções (Router) ---
        # Direciona o fluxo de execução com base na intenção identificada
        if intent_name == 'duvida_tecnica':
            # Caso seja uma dúvida técnica, aciona o fluxo RAG (Retrieval-Augmented Generation)
            response_text = handle_rag_query(user_query)
        
        elif intent_name == 'abrir_chamado':
            # Caso seja solicitação de abertura de chamado, integra com o Backend Django
            response_text = handle_create_ticket(parameters)
            
        elif intent_name == 'gerar_orcamento':
            # Caso seja solicitação de orçamento, executa a lógica de precificação
            response_text = handle_budget_quote(parameters)

        # --- Resposta para o Dialogflow ---
        # Formata a resposta no padrão esperado pelo Webhook do Dialogflow ES
        return {
            'statusCode': 200,
            'body': json.dumps({
                'fulfillmentText': response_text
            })
        }

    except Exception as e:
        # Loga a exceção completa para depuração no CloudWatch
        logger.error(f"Erro no processamento: {str(e)}", exc_info=True)
        # Retorna uma mensagem de erro genérica para o usuário final
        return {
            'statusCode': 500,
            'body': json.dumps({'fulfillmentText': 'Erro interno no servidor Nexus AI. Por favor, tente novamente mais tarde.'})
        }

def search_opensearch(query):
    """
    Executa uma busca no Amazon OpenSearch para encontrar documentos relevantes.
    Serve como a etapa de "Recuperação" (Retrieval) no pipeline RAG.
    """
    # Verifica se o host do OpenSearch está configurado
    if not OPENSEARCH_HOST:
        logger.warning("OPENSEARCH_HOST não configurado. Retornando contexto simulado.")
        return "Manual técnico do servidor: Reinicie o serviço se a luz vermelha piscar."

    client = get_opensearch_client()
    
    # Constrói a query DSL do OpenSearch.
    # Em um cenário ideal, usaríamos busca vetorial (k-NN) comparando embeddings.
    # Aqui, usamos uma busca textual simples (match) para simplificação do exemplo.
    search_query = {
        "size": 3, # Retorna os top 3 documentos mais relevantes
        "query": {
            "match": {
                "content": query # Busca o termo da query no campo 'content' dos documentos
            }
        }
    }

    try:
        # Executa a busca no índice configurado
        response = client.search(
            body=search_query,
            index=OPENSEARCH_INDEX
        )
        
        # Processa os resultados (hits)
        hits = response['hits']['hits']
        # Concatena o conteúdo dos documentos encontrados para formar o contexto
        context_parts = [hit['_source']['content'] for hit in hits]
        return "\n\n".join(context_parts)
    except Exception as e:
        logger.error(f"Erro na busca do OpenSearch: {e}")
        return ""

def handle_rag_query(query):
    """
    Fluxo RAG (Retrieval-Augmented Generation) completo:
    1. Retrieval: Busca informações relevantes na base de conhecimento (OpenSearch).
    2. Augmentation: Constrói um prompt enriquecido com o contexto recuperado.
    3. Generation: Envia o prompt para o LLM (Claude) gerar a resposta final.
    """
    # Passo 1: Recuperação de Contexto
    context_docs = search_opensearch(query)
    
    if not context_docs:
        context_docs = "Nenhuma informação específica encontrada na base de conhecimento interna."

    # Passo 2: Engenharia de Prompt (Prompt Engineering)
    # Define a persona do assistente e instrui a usar apenas o contexto fornecido (Grounding)
    prompt = f"""Human: Você é um assistente técnico especialista da Nexus AI. Use o contexto abaixo para responder à pergunta do usuário de forma útil, precisa e concisa. Se a resposta não estiver no contexto, diga que não sabe, não invente informações (alucinação).
    
    Contexto:
    {context_docs}
    
    Pergunta: {query}
    
    Assistant:"""

    # Configuração do payload para o modelo Anthropic Claude v2
    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 500, # Limite de tamanho da resposta
        "temperature": 0.3, # Baixa temperatura para respostas mais determinísticas e factuais
        "top_p": 0.9,
    })

    try:
        # Passo 3: Geração (Inferência)
        response = bedrock_client.invoke_model(
            modelId='anthropic.claude-v2', # Identificador do modelo no Bedrock
            body=body
        )
        
        # Processa a resposta do modelo
        response_body = json.loads(response['body'].read())
        return response_body['completion'].strip()
    except Exception as e:
        logger.error(f"Erro ao invocar Bedrock: {e}")
        return "Desculpe, estou tendo dificuldades para processar sua pergunta no momento devido a uma instabilidade no sistema de IA."

def handle_create_ticket(params):
    """
    Integração com o Backend Django para criação de tickets de suporte.
    Envia uma requisição HTTP POST para a API REST do sistema core.
    """
    # Extração segura de parâmetros recebidos do Dialogflow
    customer_name = params.get('person', {}).get('name', 'Cliente Não Identificado')
    problem_description = params.get('problem_description', 'Sem descrição fornecida')
    
    # Monta o payload JSON conforme esperado pelo Serializer do Django
    payload = {
        "customer_name": customer_name,
        "problem_description": problem_description,
        "status": "OPEN"
    }

    try:
        # Realiza a chamada HTTP para a API interna
        # Timeout configurado para 5s para evitar que o Lambda exceda seu tempo de execução
        response = requests.post(f"{DJANGO_API_URL}/tickets/", json=payload, timeout=5)
        
        if response.status_code == 201:
            # Sucesso: Retorna o ID do ticket criado
            ticket_id = response.json().get('id', 'N/A')
            return f"Chamado criado com sucesso! ID do ticket: #{ticket_id}. Nossa equipe entrará em contato em breve."
        else:
            # Erro na API: Loga o erro e informa o usuário
            logger.error(f"Erro na API Django: {response.status_code} - {response.text}")
            return "Tivemos um problema técnico ao registrar seu chamado. Por favor, tente novamente mais tarde."
    except requests.RequestException as e:
        # Erro de Conexão: Loga e informa o usuário
        logger.error(f"Falha de conexão com API Django: {e}")
        return "Erro de comunicação com o sistema de chamados. Tente mais tarde."

def handle_budget_quote(params):
    """
    Lógica de negócio para geração automática de orçamentos.
    Calcula valores com base em regras predefinidas e simula o envio de uma proposta.
    """
    # Extrai o tipo de serviço solicitado
    service_type = params.get('service_type', 'Consultoria Padrão')
    
    # Lógica de precificação simples (Mock)
    base_price = 1000.00
    if 'premium' in str(service_type).lower():
        base_price *= 1.5 # Adicional de 50% para serviços Premium
    
    # Em produção, aqui seria invocado um serviço de geração de PDF (ex: ReportLab ou API externa)
    # e envio de email (ex: Amazon SES).
    # generate_pdf_and_email(customer_email, service_type, base_price)
    
    return f"O orçamento estimado para {service_type} é de R$ {base_price:.2f}. Um PDF detalhado com a proposta comercial foi enviado para seu e-mail cadastrado."
