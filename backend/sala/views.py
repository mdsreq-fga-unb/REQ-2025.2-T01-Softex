from rest_framework import viewsets, permissions
from .models import Sala
from .serializers import SalaSerializer
from reserva.models import Reserva

class SalaViewSet(viewsets.ModelViewSet):
    serializer_class = SalaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Sala.objects.all().prefetch_related('reservas')
        return queryset
    

    


