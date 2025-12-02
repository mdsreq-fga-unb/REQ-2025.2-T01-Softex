FROM node:22.12-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

# Caso você tenha dependências adicionais específicas
# RUN npm install axios@1.13.2

COPY . .

# Gera o build de produção
RUN npm run build

# Instala servidor estático
RUN npm install -g serve

EXPOSE 5173

# Executa o servidor Node servindo o build
CMD ["serve", "-s", "dist", "-l", "5173"]
