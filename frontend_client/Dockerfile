# Usa uma imagem Node.js 18 baseada em Alpine Linux
# Alpine é escolhido por ser extremamente leve (~5MB base) e seguro
FROM node:18-alpine

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de definição de dependências
# O asterisco em package-lock.json* permite que o comando funcione mesmo se o arquivo não existir
COPY package.json package-lock.json* ./

# Instala as dependências do projeto
# Instala todas as dependências listadas no package.json
RUN npm install

# Copia o restante do código fonte para o container
# Note: É importante ter um .dockerignore para não copiar node_modules locais
COPY . .

# Expõe a porta 3000, padrão do Next.js, para comunicação externa
EXPOSE 3000

# Comando padrão para iniciar o servidor em modo de desenvolvimento
# Permite Hot Reloading quando usado com volumes no Docker Compose
CMD ["npm", "run", "dev"]
