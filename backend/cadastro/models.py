from django.db import models
from permissoes.models import PerfilDePermissao
from django.contrib.auth.models import AbstractUser

class Cadastro(AbstractUser):
    #na esquerda vai pro banco na direita vai pro admin ou forms 
    FUNCAO_CHOICES = [
        ('colaborador', 'Colaborador'),
        ('TI', 'TI'),
        ('Financiro', 'Financeiro'),
        ('Marketing', 'Marketing'),
        ('Juridíco', 'Juridíco'),
        ('Administrativo', 'Administrativo'),
        ('Projeto', 'Projeto'),
    ]
    #abastractuser já tem todos os dados necessários para um login, por isso herdamos dele não de uma models


    email = models.EmailField(unique=True)
    tipo_funcao = models.CharField(
        max_length=50,
        choices=FUNCAO_CHOICES,
        blank=False,
        default='administrativo',  
          )
    
    perfil = models.ForeignKey(
        'permissoes.PerfilDePermissao',
        on_delete=models.SET_NULL, 
        null=True,                
        blank=True,                
        related_name='usuarios',   
        verbose_name="Perfil de Acesso"
    )
    
    acessoBasico = models.BooleanField(default=True, verbose_name="Acesso Básico")
    dashboards = models.BooleanField(default=False, verbose_name="Dashboards")
    salasReuniao = models.BooleanField(default=False, verbose_name="Salas de Reunião")
    administracao = models.BooleanField(default=False, verbose_name="Administração")

    #configuração de login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


    def __str__(self):
        return (f"Nome: {self.first_name}\n"
                f"Sobrenome: {self.last_name}\n"
                f"email: {self.email}\n"
                f"Permissao: {self.tipo_funcao}\n")

    class Meta:
        # O django organiza automaticamente
        pass
    