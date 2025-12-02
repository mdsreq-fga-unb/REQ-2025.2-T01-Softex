from django.db import models

class PerfilDePermissao(models.Model):
    # Campos que correspondem à interface do Vue.js
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Perfil")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    
    # Permissões booleanas
    acessoBasico = models.BooleanField(default=True, verbose_name="Acesso Básico")
    dashboards = models.BooleanField(default=False, verbose_name="Dashboards")
    salasReuniao = models.BooleanField(default=False, verbose_name="Salas de Reunião")
    administracao = models.BooleanField(default=False, verbose_name="Administração")
    
    class Meta:
        verbose_name = "Perfil de Permissão"
        verbose_name_plural = "Perfis de Permissão"
        
    def __str__(self):
        return self.nome