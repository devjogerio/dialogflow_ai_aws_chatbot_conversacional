#!/bin/sh

# Verifica se o banco de dados é PostgreSQL e aguarda sua inicialização
# Isso previne que o Django tente conectar antes do banco estar pronto
if [ "$DB_ENGINE" = "django.db.backends.postgresql" ]
then
    echo "Aguardando pelo PostgreSQL..."

    # Loop que verifica a porta do banco (definida em DB_HOST e DB_PORT)
    # nc -z verifica se a porta está aberta sem enviar dados
    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL iniciado com sucesso"
fi

# Executa as migrações do banco de dados para garantir que o schema esteja atualizado
# Isso cria as tabelas necessárias no banco de dados
echo "Aplicando migrações do banco de dados..."
python manage.py migrate

# Inicia o servidor de desenvolvimento do Django acessível externamente (0.0.0.0)
# exec "$@" permite que o comando passado no CMD do Dockerfile assuma o PID 1
exec "$@"
