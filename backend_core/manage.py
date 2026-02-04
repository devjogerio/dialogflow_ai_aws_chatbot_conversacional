#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    # Define o módulo de configurações padrão do Django para 'core.settings'
    # Isso informa ao Django onde encontrar as configurações do projeto (banco de dados, apps, etc.)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        # Tenta importar a função de execução de linha de comando do Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Lança um erro explicativo se o Django não estiver instalado ou o ambiente virtual não estiver ativado
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Executa o comando passado via linha de comando (ex: runserver, migrate)
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    # Ponto de entrada do script
    main()
