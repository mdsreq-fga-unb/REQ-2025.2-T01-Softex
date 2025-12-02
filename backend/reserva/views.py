from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Reserva, ReservaCadeira
from .serializers import ReservaSerializer, ReservaCadeiraSerializer

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer


class ReservaCadeiraViewSet(viewsets.ModelViewSet):
    serializer_class = ReservaCadeiraSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]  # Usar autenticação JWT
    
    def get_queryset(self):
        # Usuários podem ver apenas suas próprias reservas
        # Admins podem ver todas
        user = self.request.user
        queryset = ReservaCadeira.objects.select_related('usuario', 'cadeira', 'cadeira__sala')
        
        if not user.is_staff:
            queryset = queryset.filter(usuario=user)
        
        return queryset.order_by('-data_criacao')
    
    def perform_create(self, serializer):
        # Automaticamente associa a reserva ao usuário autenticado via JWT
        user = self.request.user
        
        if not user.is_authenticated:
            from rest_framework.exceptions import AuthenticationFailed
            raise AuthenticationFailed('Usuário não autenticado')
        
        # Garantir que o usuário do payload não sobrescreva o usuário autenticado
        validated_data = serializer.validated_data.copy()
        validated_data.pop('usuario', None)  # Remove se existir
        validated_data['usuario'] = user  # Força o usuário autenticado
        
        serializer.save(**validated_data)