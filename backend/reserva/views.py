from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .models import Reserva, ReservaCadeira
from .serializers import ReservaSerializer, ReservaCadeiraSerializer

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Classe de autenticação que desabilita CSRF para APIs
    """
    def enforce_csrf(self, request):
        return  # Não aplicar verificação de CSRF


class ReservaCadeiraViewSet(viewsets.ModelViewSet):
    serializer_class = ReservaCadeiraSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]  # Usar autenticação sem CSRF
    
    def get_queryset(self):
        # Usuários podem ver apenas suas próprias reservas
        # Admins podem ver todas
        user = self.request.user
        queryset = ReservaCadeira.objects.select_related('usuario', 'cadeira', 'cadeira__sala')
        
        if not user.is_staff:
            queryset = queryset.filter(usuario=user)
        
        return queryset.order_by('-data_criacao')
    
    def perform_create(self, serializer):
        # Automaticamente associa a reserva ao usuário autenticado
        serializer.save(usuario=self.request.user)