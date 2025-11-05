from django.db import models
from django.contrib.auth.models import AbstractUser

class Cadastro(AbstractUser):
    #na esquerda vai pro banco na direita vai pro admin ou forms 
    PERMISSAO_CHOICES = [
        ('colaborador', 'Colaborador'),
        ('lider', 'Lider'),
        ('rh', 'RH'),
        ('admin', 'Admin'),
    ]
    #abastractuser já tem todos os dados necessários para um login, por isso herdamos dele não de uma models


    email = models.EmailField(unique=True)
    tipo_permissao = models.CharField(
        max_length=50,
        choices=PERMISSAO_CHOICES,
        blank=False,
        default='colaborador',  
          )

    #configuração de login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


    def __str__(self):
        return (f"Nome: {self.first_name}\n"
                f"Sobrenome: {self.last_name}\n"
                f"email: {self.email}\n"
                f"Permissao: {self.tipo_permissao}\n")

    class Meta:
        # O django organiza automaticamente
        pass
    