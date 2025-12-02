from rest_framework import viewsets, permissions, mixins
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
