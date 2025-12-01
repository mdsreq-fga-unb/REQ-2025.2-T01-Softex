FROM node:22.12-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

RUN npm install axios@1.13.2
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
