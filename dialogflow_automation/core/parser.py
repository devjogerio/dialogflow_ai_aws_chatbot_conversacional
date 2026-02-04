import json
import os
from .logger import setup_logger

# Inicializa o logger para este módulo
logger = setup_logger("config_parser")

class ConfigParser:
    """
    Classe responsável por ler e validar arquivos de configuração (Intents, Entidades).
    Centraliza o acesso aos dados JSON que definem a estrutura do Chatbot.
    """

    def __init__(self, config_path):
        """
        Inicializa o parser com o caminho para o diretório de configuração.
        
        Args:
            config_path (str): Caminho relativo ou absoluto para a pasta de configs.
        """
        self.config_path = config_path
        # Valida se o diretório existe imediatamente
        if not os.path.exists(self.config_path):
            logger.error(f"Diretório de configuração não encontrado: {self.config_path}")
            raise FileNotFoundError(f"Config path not found: {self.config_path}")

    def load_intents(self, filename="intents.json"):
        """
        Carrega e valida a lista de intenções do arquivo JSON.
        
        Args:
            filename (str): Nome do arquivo JSON contendo as intenções.
            
        Returns:
            list: Lista de dicionários contendo a definição das intenções.
        """
        file_path = os.path.join(self.config_path, filename)
        logger.info(f"Carregando intenções de: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                intents = json.load(f)
                
            # Validação básica de esquema
            if not isinstance(intents, list):
                raise ValueError("O arquivo de intents deve conter uma lista JSON.")
            
            logger.info(f"{len(intents)} intenções carregadas com sucesso.")
            return intents
            
        except FileNotFoundError:
            logger.error(f"Arquivo de intenções não encontrado: {file_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Erro de sintaxe no JSON de intenções: {e}")
            raise
