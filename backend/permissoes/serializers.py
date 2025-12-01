# permissoes/serializers.py

from rest_framework import serializers
from .models import PerfilDePermissao

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