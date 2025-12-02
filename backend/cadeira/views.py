from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Cadeira
from .serializers import CadeiraSerializer


class CadeiraViewSet(viewsets.ModelViewSet):
    serializer_class = CadeiraSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        queryset = Cadeira.objects.all().select_related('sala')
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        """
        Permite exclusão apenas para usuários Administrativo
        """
        user = request.user
        
        if not user.is_authenticated:
            from rest_framework.exceptions import AuthenticationFailed
            raise AuthenticationFailed('Usuário não autenticado')
        
        # Verificar se o usuário é Administrativo
        if user.tipo_funcao != 'Administrativo':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Apenas administradores podem excluir cadeiras.')
        
        instance = self.get_object()
        self.perform_destroy(instance)
        
        from rest_framework.response import Response
        from rest_framework import status
        return Response(
            {"detail": f"Cadeira {instance.id_cadeira} excluída com sucesso."},
            status=status.HTTP_200_OK
        )
