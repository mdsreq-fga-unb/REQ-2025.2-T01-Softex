from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from django.db.models import Count, Q
from django.db.models.functions import ExtractHour

# Imports dos seus Models e Serializers
from .models import Reserva, ReservaCadeira
from .serializers import ReservaSerializer, ReservaCadeiraSerializer
from sala.models import Sala
from cadeira.models import Cadeira


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        # Usuários podem ver apenas suas próprias reservas
        # Admins podem ver todas
        user = self.request.user
        queryset = Reserva.objects.select_related('usuario', 'sala', 'sala__planta')
        
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


class ReservaCadeiraViewSet(viewsets.ModelViewSet):
    serializer_class = ReservaCadeiraSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        user = self.request.user
        queryset = ReservaCadeira.objects.select_related('usuario', 'cadeira', 'cadeira__sala')
        
        # Se for GET e o usuário não for admin, filtrar apenas suas reservas
        if self.request.method == 'GET' and not user.is_staff:
            queryset = queryset.filter(usuario=user)
        
        return queryset.order_by('-data_criacao')
    
    def get_serializer_context(self):
        """
        Adiciona o request ao contexto do serializer para validações
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    @action(detail=False, methods=['get'], url_path='disponibilidade')
    def disponibilidade(self, request):
        """
        Endpoint para verificar disponibilidade de cadeiras
        Retorna todas as reservas confirmadas (para verificar conflitos)
        """
        reservas_confirmadas = ReservaCadeira.objects.filter(
            status='confirmada'
        ).select_related('usuario', 'cadeira')
        
        serializer = self.get_serializer(reservas_confirmadas, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        user = self.request.user
        
        if not user.is_authenticated:
            from rest_framework.exceptions import AuthenticationFailed
            raise AuthenticationFailed('Usuário não autenticado')
        
        validated_data = serializer.validated_data.copy()
        validated_data.pop('usuario', None)
        validated_data['usuario'] = user
        
        serializer.save(**validated_data)


# --- VIEW DO DASHBOARD CORRIGIDA ---
class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        # 1. Definições de Tempo
        agora = timezone.now()
        hoje = agora.date()
        hora_atual = agora.time()

        # 2. Capacidade Total
        # Pega do banco ou usa fallback se estiver vazio
        total_salas = Sala.objects.count() or 6 
        total_cadeiras = Cadeira.objects.count() or 58
        capacidade_total = total_salas + total_cadeiras

        # ---------------------------------------------------------
        # 3. Métricas de SALAS (Reserva Model)
        # ---------------------------------------------------------
        
        # Salas ocupadas NESTE MOMENTO (DateTime)
        salas_em_uso = Reserva.objects.filter(
            data_inicio__lte=agora,
            data_fim__gte=agora,
            status='confirmada'
        ).count()

        # Total de reservas de sala HOJE
        reservas_sala_hoje = Reserva.objects.filter(
            data_inicio__date=hoje,
            status='confirmada'
        ).count()

        # Distribuição por Horário (Salas)
        distrib_sala_hora = Reserva.objects.filter(
            data_inicio__date=hoje, status='confirmada'
        ).annotate(
            hora=ExtractHour('data_inicio')
        ).values('hora').annotate(total=Count('id_reserva')).order_by('hora')

        # ---------------------------------------------------------
        # 4. Métricas de CADEIRAS (ReservaCadeira Model)
        # ---------------------------------------------------------

        # Cadeiras ocupadas NESTE MOMENTO (Date + Time)
        cadeiras_ocupadas = ReservaCadeira.objects.filter(
            data_inicio=hoje,
            hora_inicio__lte=hora_atual,
            hora_fim__gte=hora_atual,
            status='confirmada'
        ).count()

        # Total de reservas de cadeira HOJE
        reservas_cadeira_hoje = ReservaCadeira.objects.filter(
            data_inicio=hoje,
            status='confirmada'
        ).count()

        # Distribuição por Horário (Cadeiras)
        distrib_cadeira_hora = ReservaCadeira.objects.filter(
            data_inicio=hoje, status='confirmada'
        ).annotate(
            hora=ExtractHour('hora_inicio')
        ).values('hora').annotate(total=Count('id_reserva_cadeira')).order_by('hora')

        # ---------------------------------------------------------
        # 5. Cálculos de Porcentagem e Consolidação
        # ---------------------------------------------------------

        taxa_ocupacao_sala = round((salas_em_uso / total_salas * 100), 1) if total_salas > 0 else 0
        taxa_ocupacao_cadeira = round((cadeiras_ocupadas / total_cadeiras * 100), 1) if total_cadeiras > 0 else 0
        
        ocupados_total = salas_em_uso + cadeiras_ocupadas
        taxa_ocupacao_geral = round((ocupados_total / capacidade_total * 100), 1) if capacidade_total > 0 else 0

        # Distribuição de Uso (Gráfico de Rosca)
        pct_uso_salas = round((salas_em_uso / capacidade_total * 100), 1) if capacidade_total > 0 else 0
        pct_uso_coworking = round((cadeiras_ocupadas / capacidade_total * 100), 1) if capacidade_total > 0 else 0
        pct_livre = round(100 - pct_uso_salas - pct_uso_coworking, 1)

        # ---------------------------------------------------------
        # 6. Formatação dos Gráficos de Horário
        # ---------------------------------------------------------
        
        def formatar_grafico_horario(dados_banco, capacidade_item):
            # Cria mapa das 8h as 19h zerado
            mapa_horas = {h: 0 for h in range(8, 20)}
            
            for item in dados_banco:
                h = item['hora']
                if h in mapa_horas:
                    mapa_horas[h] = round((item['total'] / capacidade_item * 100), 1)
            
            # Formata array para o Vue (apenas horas pares para ficar limpo: 8h, 10h...)
            return [
                {"hora": f"{h}h", "porcentagem": mapa_horas[h]} 
                for h in range(8, 20, 2) 
            ]

        grafico_salas_formatado = formatar_grafico_horario(distrib_sala_hora, total_salas)
        grafico_cadeiras_formatado = formatar_grafico_horario(distrib_cadeira_hora, total_cadeiras)
        
        # Cria média para o gráfico "Todos"
        grafico_todos = []
        for i in range(len(grafico_salas_formatado)):
            s = grafico_salas_formatado[i]
            c = grafico_cadeiras_formatado[i]
            media = round((s['porcentagem'] + c['porcentagem']) / 2, 1)
            grafico_todos.append({"hora": s['hora'], "porcentagem": media})

        # ---------------------------------------------------------
        # 7. Retorno JSON
        # ---------------------------------------------------------
        return Response({
            "metricas": {
                "sala": {
                    "posicoes_ocupadas": 0,
                    "salas_em_uso": salas_em_uso,
                    "total_salas": total_salas,
                    "reservas_hoje": reservas_sala_hoje,
                    "taxa_ocupacao": taxa_ocupacao_sala
                },
                "cadeira": {
                    "posicoes_ocupadas": cadeiras_ocupadas,
                    "total_cadeiras": total_cadeiras,
                    "salas_em_uso": 0, 
                    "reservas_hoje": reservas_cadeira_hoje,
                    "taxa_ocupacao": taxa_ocupacao_cadeira
                },
                "todas": {
                    "posicoes_ocupadas": cadeiras_ocupadas,
                    "salas_em_uso": salas_em_uso,
                    "reservas_hoje": reservas_sala_hoje + reservas_cadeira_hoje,
                    "taxa_ocupacao": taxa_ocupacao_geral
                }
            },
            "graficos": {
                "ocupacao_horario": {
                    "sala": grafico_salas_formatado,
                    "cadeira": grafico_cadeiras_formatado,
                    "todas": grafico_todos
                },
                "distribuicao_uso": {
                    "salas": pct_uso_salas,
                    "coworking": pct_uso_coworking,
                    "livre": pct_livre if pct_livre >= 0 else 0,
                    "ocupado_geral": taxa_ocupacao_geral
                }
            }
        })
