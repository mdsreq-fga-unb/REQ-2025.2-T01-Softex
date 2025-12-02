#!/bin/sh

echo "==> Esperando o Postgres subir..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Postgres pronto!"

echo "==> Aplicando migrations..."
python manage.py makemigrations
python manage.py migrate

echo "==> Criando superusuário (se não existir)..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()

email = "${DJANGO_SUPERUSER_EMAIL}"
password = "${DJANGO_SUPERUSER_PASSWORD}"
username = "${DJANGO_SUPERUSER_USERNAME}"
first_name = "${DJANGO_SUPERUSER_FIRST_NAME}"
last_name = "${DJANGO_SUPERUSER_LAST_NAME}"

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(
        email=email,
        password=password,
        username=username,
        first_name=first_name,
        last_name=last_name,
    )
    print("Superusuário criado!")
else:
    print("Superusuário já existe.")
EOF

echo "==> Iniciando o servidor Django..."
python manage.py runserver 0.0.0.0:8000
