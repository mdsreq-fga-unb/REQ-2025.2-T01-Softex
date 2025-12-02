from rest_framework import viewsets, permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Sala, SalaDeReuniao
from .serializers import SalaSerializer, SalaDeReuniaoSerializer
from reserva.models import Reserva

class SalaViewSet(viewsets.ModelViewSet):
    serializer_class = SalaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Sala.objects.all().prefetch_related('reservas')
        return queryset
    

    
class SalaDeReuniaoViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = SalaDeReuniao.objects.all().order_by('id')
    serializer_class = SalaDeReuniaoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    @action(detail=False, methods=['post'], url_path='reservar')
    def reservar(self, request):
        """
        Endpoint para criar reserva de sala de reunião
        POST /api/salas-reuniao/reservar/
        """
        try:
            sala_id = request.data.get('sala')
            data_inicio = request.data.get('data_inicio')
            data_fim = request.data.get('data_fim')
            descricao = request.data.get('descricao', '')
            
            if not sala_id:
                return Response(
                    {'error': 'ID da sala é obrigatório'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not data_inicio or not data_fim:
                return Response(
                    {'error': 'data_inicio e data_fim são obrigatórios'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Buscar a sala de reunião
            try:
                sala_reuniao = SalaDeReuniao.objects.get(id=sala_id)
            except SalaDeReuniao.DoesNotExist:
                return Response(
                    {'error': f'Sala de reunião com id {sala_id} não encontrada'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Verificar se existe uma Sala correspondente (com tipo="reuniao")
            # Se não existir, criar uma Sala temporária ou usar uma existente
            # Por enquanto, vamos procurar uma Sala com tipo="reuniao" que corresponda
            # ou criar uma reserva usando o modelo Reserva mas precisamos adaptar
            
            # Como o modelo Reserva precisa de uma Sala (não SalaDeReuniao),
            # vamos criar ou buscar uma Sala correspondente
            from planta.models import Planta
            # Buscar a primeira planta disponível ou criar uma lógica
            planta = Planta.objects.first()
            
            if not planta:
                return Response(
                    {'error': 'Nenhuma planta cadastrada. É necessário cadastrar uma planta primeiro.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Buscar ou criar uma Sala correspondente à SalaDeReuniao
            sala, created = Sala.objects.get_or_create(
                nome_sala=sala_reuniao.nome,
                tipo='reuniao',
                defaults={
                    'capacidade': 0,
                    'descricao': f'Sala de reunião: {sala_reuniao.nome}',
                    'planta': planta
                }
            )
            
            # Criar a reserva
            reserva = Reserva.objects.create(
                usuario=request.user,
                sala=sala,
                data_inicio=data_inicio,
                data_fim=data_fim,
                descricao=descricao,
                status='confirmada'
            )
            
            from reserva.serializers import ReservaSerializer
            serializer = ReservaSerializer(reserva)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
