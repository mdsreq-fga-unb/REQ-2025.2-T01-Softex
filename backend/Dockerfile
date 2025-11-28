FROM python:3.11-slim

# Variáveis para evitar buffering e manter logs visíveis
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y build-essential libpq-dev && apt-get clean

# Criar diretório da aplicação
WORKDIR /app

# Copiar requirements
COPY requirements.txt /app/

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . /app/

# Expor porta
EXPOSE 8000

# Comando padrão
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
