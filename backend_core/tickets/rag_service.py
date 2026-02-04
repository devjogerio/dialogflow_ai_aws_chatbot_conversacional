import boto3
import json
import os
import logging
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from django.conf import settings

logger = logging.getLogger(__name__)

# --- Configurações ---
BEDROCK_REGION = os.environ.get('AWS_REGION', 'us-east-1')
OPENSEARCH_HOST = os.environ.get('OPENSEARCH_HOST')
OPENSEARCH_INDEX = os.environ.get('OPENSEARCH_INDEX', 'knowledge-base')

def get_opensearch_client():
    """
    Cria e retorna um cliente OpenSearch configurado com autenticação AWS (SigV4).
    """
    if not OPENSEARCH_HOST:
        return None
        
    region = BEDROCK_REGION
    service = 'es'
    credentials = boto3.Session().get_credentials()
    
    if not credentials:
        logger.warning("Credenciais AWS não encontradas. OpenSearch não será inicializado.")
        return None

    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    return OpenSearch(
        hosts=[{'host': OPENSEARCH_HOST, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

def search_opensearch(query):
    """
    Executa busca no OpenSearch.
    """
    client = get_opensearch_client()
    if not client:
        return "Manual técnico do servidor: Reinicie o serviço se a luz vermelha piscar. (Contexto Simulado - Sem conexão OpenSearch)"

    search_query = {
        "size": 3,
        "query": {
            "match": {
                "content": query
            }
        }
    }

    try:
        response = client.search(body=search_query, index=OPENSEARCH_INDEX)
        hits = response['hits']['hits']
        context_parts = [hit['_source']['content'] for hit in hits]
        return "\n\n".join(context_parts)
    except Exception as e:
        logger.error(f"Erro na busca do OpenSearch: {e}")
        return ""

def generate_bedrock_response(query, context):
    """
    Gera resposta usando Amazon Bedrock (Claude v2).
    """
    bedrock_client = boto3.client(service_name='bedrock-runtime', region_name=BEDROCK_REGION)
    
    prompt = f"""Human: Você é um assistente técnico especialista da Nexus AI. Use o contexto abaixo para responder à pergunta do usuário de forma útil, precisa e concisa. Se a resposta não estiver no contexto, diga que não sabe.
    
    Contexto:
    {context}
    
    Pergunta: {query}
    
    Assistant:"""

    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 500,
        "temperature": 0.3,
        "top_p": 0.9,
    })

    try:
        response = bedrock_client.invoke_model(
            modelId='anthropic.claude-v2',
            body=body
        )
        response_body = json.loads(response['body'].read())
        return response_body['completion'].strip()
    except Exception as e:
        logger.error(f"Erro ao invocar Bedrock: {e}")
        # Fallback para dev local sem credenciais
        return f"Simulação local (Erro Bedrock): {query} - Resposta baseada no contexto: {context[:50]}..."

def process_chat_message(message):
    """
    Orquestra o fluxo RAG.
    """
    # 1. Recuperação
    context = search_opensearch(message)
    if not context:
        context = "Nenhuma informação específica encontrada."

    # 2. Geração
    answer = generate_bedrock_response(message, context)
    return answer
