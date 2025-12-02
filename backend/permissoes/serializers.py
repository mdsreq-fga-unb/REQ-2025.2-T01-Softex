# permissoes/serializers.py

from rest_framework import serializers
from .models import PerfilDePermissao
from cadastro.models import Cadastro

class PerfilPermissaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilDePermissao
        fields = [
            'id', 
            'nome', 
            'descricao', 
            'acessoBasico', 
            'dashboards', 
            'salasReuniao', 
            'administracao'
        ]
        read_only_fields = ['id']
        
class UsuarioGerenciamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cadastro
        fields = [
            'id', 
            'first_name', 
            'last_name', 
            'email', 
            'tipo_funcao',
            # As permissões agora são campos normais, fáceis de ler e escrever
            'acessoBasico', 
            'dashboards', 
            'salasReuniao', 
            'administracao'
        ]
        # Dica: Proteja campos sensíveis para não serem alterados sem querer
        read_only_fields = ['id', 'email']