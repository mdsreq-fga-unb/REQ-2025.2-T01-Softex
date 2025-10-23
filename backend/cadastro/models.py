from django.db import models

class Cadastro(models.Model):
    #na esquerda vai pro banco na direita vai pro admin ou forms 
    PERMISSAO_CHOICES = [
        ('colaborador', 'Colaborador'),
        ('lider', 'Lider'),
        ('rh', 'RH'),
        ('admin', 'Admin'),
    ]


    id_cadastro = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    tipo_permissao = models.CharField(max_length=50, choices=PERMISSAO_CHOICES, blank=False)

    def __str__(self):
        return f"Nome: {self.nome}\n Sobrenome: {self.sobrenome}\n email: {self.email} \n Permissao: {self.tipo_permissao}\n"
    