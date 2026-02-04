import os
from google.cloud import dialogflow_v2 as dialogflow
from google.api_core.exceptions import AlreadyExists, GoogleAPICallError
from .logger import setup_logger

# Inicializa o logger para o cliente Dialogflow
logger = setup_logger("dialogflow_client")

class DialogflowClient:
    """
    Wrapper para a API do Google Cloud Dialogflow ES.
    Facilita a criação programática de Agentes, Intenções e Entidades.
    """

    def __init__(self, project_id, service_account_path):
        """
        Inicializa o cliente com as credenciais do Google Cloud.
        
        Args:
            project_id (str): ID do projeto no Google Cloud.
            service_account_path (str): Caminho para o arquivo JSON da Service Account.
        """
        self.project_id = project_id
        
        # Define a variável de ambiente para autenticação do Google
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_path
        
        # Inicializa o cliente de intenções
        self.intents_client = dialogflow.IntentsClient()
        # Define o caminho "pai" (parent) que representa o agente no projeto
        self.parent = f"projects/{project_id}/agent"
        
        logger.info(f"Cliente Dialogflow inicializado para o projeto: {project_id}")

    def create_intent(self, display_name, training_phrases_parts, message_texts, parameters=None):
        """
        Cria uma nova intenção (Intent) no Dialogflow.
        
        Args:
            display_name (str): Nome de exibição da intenção.
            training_phrases_parts (list): Lista de frases de treinamento (strings).
            message_texts (list): Lista de respostas textuais do bot.
            parameters (list, optional): Lista de dicionários definindo parâmetros/entidades.
        """
        logger.info(f"Criando intenção: {display_name}")

        try:
            # 1. Constrói as frases de treinamento (Training Phrases)
            training_phrases = []
            for phrase_text in training_phrases_parts:
                part = dialogflow.Intent.TrainingPhrase.Part(text=phrase_text)
                training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
                training_phrases.append(training_phrase)

            # 2. Constrói a mensagem de resposta (Response Message)
            text = dialogflow.Intent.Message.Text(text=message_texts)
            message = dialogflow.Intent.Message(text=text)

            # 3. Constrói os parâmetros (Entidades a serem extraídas)
            intent_parameters = []
            if parameters:
                for param in parameters:
                    new_param = dialogflow.Intent.Parameter(
                        display_name=param['display_name'],
                        entity_type_display_name=param['entity_type_display_name'],
                        mandatory=param.get('mandatory', False),
                        prompts=param.get('prompts', [])
                    )
                    intent_parameters.append(new_param)

            # 4. Monta o objeto Intent completo
            intent = dialogflow.Intent(
                display_name=display_name,
                training_phrases=training_phrases,
                messages=[message],
                parameters=intent_parameters
            )

            # 5. Chama a API para criar a intenção
            response = self.intents_client.create_intent(
                request={"parent": self.parent, "intent": intent}
            )

            logger.info(f"Intenção criada com sucesso: {response.name}")
            return response

        except AlreadyExists:
            logger.warning(f"A intenção '{display_name}' já existe. Ignorando criação.")
        except GoogleAPICallError as e:
            logger.error(f"Erro ao chamar API do Dialogflow: {e}")
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao criar intenção '{display_name}': {e}")
            raise

    def list_intents(self):
        """
        Lista todas as intenções existentes no agente.
        Útil para validação ou limpeza antes do sync.
        """
        logger.info("Listando intenções existentes...")
        intents = self.intents_client.list_intents(request={"parent": self.parent})
        for intent in intents:
            logger.info(f"Encontrada: {intent.display_name} (ID: {intent.name})")
        return intents
