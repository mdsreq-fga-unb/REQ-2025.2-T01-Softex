from rest_framework import viewsets, permissions
from .models import Cadeira
from .serializers import CadeiraSerializer


class CadeiraViewSet(viewsets.ModelViewSet):
    serializer_class = CadeiraSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Cadeira.objects.all().select_related('sala')
        return queryset
