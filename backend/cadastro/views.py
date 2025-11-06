from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Cadastro
from .serializers import CadastroSerializer

class CadastroViewSet(viewsets.ModelViewSet):
    queryset = Cadastro.objects.all().order_by('id')
    serializer_class = CadastroSerializer

    #definindo as permições de ação
    def get_permissions(self):
        # se for criação de novo usuário, permite que qualquer um se registre
        if self.action == 'create':
            permissions_classes = [permissions.AllowAny]

        else:
            # para as outras ações exige que o user seja adm
            permissions_classes = [permissions.IsAdminUser]
        
        return [permissions() for permissions in permissions_classes]